#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import sys
import logging 

class LstmRegression(object):
    def __init__(self,
                 input_size=1,
                 output_size=1,
                 batch_size=500,
                 lstm_hide_size=256,
                 lstm_depth=5,
                 lstm_learning_rate=0.01,
                 lstm_time_step=16,
                 gradient_clipping=5,
                 train_drop_out=0.5):
        self.__input_size = input_size
        self.__output_size = output_size
        self.__batch_size = batch_size
        self.__lstm_hide_size = lstm_hide_size
        self.__lstm_depth = lstm_depth
        self.__lstm_learning_rate = lstm_learning_rate
        self.__lstm_time_step = lstm_time_step
        self.__gradient_clipping = gradient_clipping
        self.__train_drop_out = train_drop_out
        self.__build_lstm_network()
        # Logger configuration
        self.__logger = logging.getLogger("LSTM Logger")
        self.__logger.setLevel(logging.INFO)
        sh = logging.StreamHandler(sys.stdout)
        fmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)
        sh.setFormatter(formatter)
        self.__logger.addHandler(sh)
        # Forbid logger propagate to upper console logger
        self.__logger.propagate = False
        
    def __build_inputs(self):
        with tf.name_scope("inputs"):
            self.__input = tf.placeholder(tf.float32, shape=(
                self.__batch_size, self.__lstm_time_step, self.__input_size), name="input")
            self.__target = tf.placeholder(tf.float32, shape=(
                self.__batch_size, self.__output_size), name="target")
            self.__drop_out = tf.placeholder(tf.float32, name="drop_out")
    
    # Build a single lstm cell 
    def __get_a_cell(self, lstm_hide_size, drop_out):
        lstm = tf.nn.rnn_cell.BasicLSTMCell(lstm_hide_size, state_is_tuple=True)
        drop = tf.nn.rnn_cell.DropoutWrapper(cell=lstm, output_keep_prob=drop_out)
        return drop
    
    # Stacking mutiple lstm cell
    def __stacking_network(self):
        with tf.name_scope("lstm"):
            cell = tf.nn.rnn_cell.MultiRNNCell(
                [self.__get_a_cell(self.__lstm_hide_size, self.__drop_out) for _ in range(self.__lstm_depth)], 
                state_is_tuple=True
            )

            self.__initial_state = cell.zero_state(batch_size=self.__batch_size, dtype=tf.float32)
            # Unrolling in time steps
            self.__lstm_output, self.__final_state = tf.nn.dynamic_rnn(cell, self.__input, initial_state=self.__initial_state)
            # Add full connect layer to get prediction
            self.__lstm_prediction = tf.contrib.layers.fully_connected(self.__final_state[-1].h, self.__output_size, 
                activation_fn=None)
    
    def __build_loss(self):
         with tf.name_scope("loss"):
            prediction = self.__lstm_prediction
            label = self.__target
            loss = tf.losses.mean_squared_error(labels=label, predictions=prediction)
            self.__loss = tf.reduce_mean(loss)

    def __build_optimizer(self):
        # Use clipping gradients
        tfvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.__loss, tfvars), self.__gradient_clipping)
        train_op = tf.train.AdamOptimizer(self.__lstm_learning_rate)
        self.__optimizer = train_op.apply_gradients(zip(grads, tfvars))
    
    # Build network
    def __build_lstm_network(self):
        tf.reset_default_graph()
        self.__build_inputs()
        self.__stacking_network()
        self.__build_loss()
        self.__build_optimizer()
        self.__saver = tf.train.Saver()
        
    def __generator(self, train_x, train_y):
        for i in range(train_x.shape[0]):
            yield train_x[i], train_y[i]

    def lstm_train(self, train_x, train_y, train_pass_num, save_path, log_every_n):
        self.__session = tf.Session()
        with self.__session as sess:
            sess.run(tf.global_variables_initializer())
            # Train network
            new_state = sess.run(self.__initial_state)
            self.__last_saved_loss = 100000.0
            for pass_num in range(train_pass_num):
                pass_total_loss = 0.0
                batch_num = 0
                for x, y in self.__generator(train_x, train_y):
                    batch_num += 1
                    feed = {  self.__input: x,
                              self.__target: y,
                              self.__drop_out: self.__train_drop_out,
                              self.__initial_state: new_state 
                           }
                    batch_loss, new_state, _, _ = sess.run([self.__loss,
                                                            self.__final_state,
                                                            self.__lstm_prediction,
                                                            self.__optimizer], feed_dict=feed)
                    pass_total_loss += batch_loss
                    # Log on console
                    if batch_num % log_every_n == 0:
                        self.__logger.info("Training Info  epoch: {}  batch: {}  loss: {:.4f}..."
                                               .format(pass_num, batch_num, batch_loss))
                # Save model
                if pass_total_loss <= self.__last_saved_loss:
                    self.__last_saved_loss = pass_total_loss
                    self.__saver.save(sess, save_path)
                    self.__logger.info("LSTM model saved.  total_loss: {:.4f}  train_epoch: {}"
                                           .format(self.__last_saved_loss, pass_num))


    def load_model(self, checkpoint):
        self.__session = tf.Session()
        self.__saver.restore(self.__session, checkpoint)
        self.__logger.info("Reload lstm model from: {}".format(checkpoint))

    def lstm_predict(self, predict_x):
        sess = self.__session
        new_state = sess.run(self.__initial_state)
        result = np.zeros((predict_x.shape[0], self.__output_size), dtype=float)
        predict_x = np.reshape(predict_x, (-1, self.__batch_size, self.__lstm_time_step, self.__input_size))
        for i in range(predict_x.shape[0]):
            sample = predict_x[i]
            feed = {  self.__input: sample,
                      self.__drop_out: 1.0,
                      self.__initial_state: new_state 
                   }
            predicts = sess.run(self.__lstm_prediction, feed_dict=feed)
            result[i] = predicts
            self.__logger.info("Predict pass: {}.".format(i+1))
        return result
    
    #  Use saved cost as grid search estimator
    def get_saved_cost(self):
        return self.__last_saved_loss

