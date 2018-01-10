#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import sys
import logging
import json
import codecs
from lstm_model import LstmRegression

class LstmGridSearch(object):
    def __init__(self,
                 normalize_data,
                 train_set_num,
                 param_path,
                 model_path,
                 param_dict,
                 epoch):
        self.__normalize = normalize_data
        self.__train_set_num = train_set_num
        self.__model_path = model_path
        self.__param_path = param_path
        self.__param_dict = param_dict
        self.__epoch = epoch
        # Logger configuration
        self.__logger = logging.getLogger("LSTM Grid Search Logger")
        self.__logger.setLevel(logging.INFO)
        sh = logging.StreamHandler(sys.stdout)
        fmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)
        sh.setFormatter(formatter)
        self.__logger.addHandler(sh)
    
    def __prepare_train_data(self,
                             train_set_num, 
                             batch_size, 
                             time_step, 
                             input_size, 
                             output_size):
        normalize = np.reshape(self.__normalize, (-1, input_size))
        x_shape = (train_set_num, time_step, input_size)
        y_shape = (train_set_num, output_size)
        train_x = np.zeros(x_shape, dtype=float)
        train_y = np.zeros(y_shape, dtype=float)
        assert train_set_num + time_step <= normalize.shape[0], "Train set is too large."
        for i in range(train_set_num):
            train_x[i, 0:, 0:] = normalize[i: i+time_step, 0:]
            train_y[i, 0:] = normalize[i+time_step, 0:]
        # Shuffle train data
        train_x = np.reshape(train_x, (-1, time_step))
        train_y = np.reshape(train_y, (-1, output_size))
        shuffle_data = np.hstack((train_x, train_y))
        np.random.shuffle(shuffle_data)
        train_x = shuffle_data[0:, 0: time_step]
        train_y = shuffle_data[0:, time_step:]
        train_x = np.reshape(train_x, (-1, batch_size, time_step, input_size))
        train_y = np.reshape(train_y, (-1, batch_size, output_size))
        return train_x, train_y
    
    def __record_optimized_param(self, optimized_dict):
        with codecs.open(self.__param_path, "w+", encoding="utf-8") as f:
            json.dump(optimized_dict, f, ensure_ascii=False, indent=4)
            f.close()
    
    def grid_search(self):
        input_size = self.__param_dict["input_size"]
        output_size = self.__param_dict["output_size"]
        list_batch_size = self.__param_dict["batch_size"]
        list_lstm_hide_size = self.__param_dict["lstm_hide_size"]
        list_lstm_depth = self.__param_dict["lstm_depth"]
        list_lstm_learning_rate = self.__param_dict["lstm_learning_rate"]
        list_time_step = self.__param_dict["lstm_time_step"]
        gradient_clipping = 5
        train_drop_out = 0.5
        # Initialize optimized param
        optimized_cost = 10000000
        op_batch_size = list_batch_size[0]
        op_lstm_hide_size = list_lstm_hide_size[0]
        op_lstm_depth = list_lstm_depth[0]
        op_lstm_learning_rate = list_lstm_learning_rate[0]
        op_lstm_time_step = list_time_step[0]
        # Grid search optimized param
        for batch_size in list_batch_size:
            for lstm_hide_size in list_lstm_hide_size:
                for lstm_depth in list_lstm_depth:
                    for lstm_learning_rate in list_lstm_learning_rate:
                        for lstm_time_step in list_time_step:
                            # Generate train data
                            train_x, train_y = self.__prepare_train_data(self.__train_set_num,
                                                                         batch_size,
                                                                         lstm_time_step, 
                                                                         input_size, 
                                                                         output_size)
                            # Initialize lstm model
                            lstm = LstmRegression(input_size=input_size,
                                                  output_size=output_size,
                                                  batch_size=batch_size,
                                                  lstm_hide_size=lstm_hide_size,
                                                  lstm_depth=lstm_depth,
                                                  lstm_learning_rate=lstm_learning_rate,
                                                  lstm_time_step=lstm_time_step,
                                                  gradient_clipping=gradient_clipping,
                                                  train_drop_out=train_drop_out)
                            
                            lstm.lstm_train(train_x, train_y, self.__epoch, self.__model_path, 1)
                            
                            last_saved_cost = lstm.get_saved_cost()
                            # Save optimized param
                            if last_saved_cost <= optimized_cost:
                                optimized_cost = last_saved_cost
                                op_batch_size = batch_size
                                op_lstm_hide_size = lstm_hide_size
                                op_lstm_depth = lstm_depth
                                op_lstm_learning_rate = lstm_learning_rate
                                op_lstm_time_step = lstm_time_step
                            log_info = "Grid Search Info.  optimized cost: {:.4f}" + \
                                       " optimized batch_size: {} optimized hide_size: {}" + \
                                       " optimized depth: {} optimized learning_rate: {} optimized time_step: {}"
                            self.__logger.info(log_info.format(optimized_cost, 
                                                               op_batch_size,
                                                               op_lstm_hide_size,
                                                               op_lstm_depth,
                                                               op_lstm_learning_rate,
                                                               op_lstm_time_step))
                                
        optimized_dict = {  "input_size": input_size,
                            "output_size": output_size,
                            "batch_size": batch_size,
                            "lstm_hide_size": lstm_hide_size,
                            "lstm_depth": lstm_depth,
                            "lstm_learning_rate": lstm_learning_rate,
                            "lstm_time_step": lstm_time_step,
                            "gradient_clipping": gradient_clipping,
                            "train_drop_out": train_drop_out
                         }
        # Write optimized param into file
        self.__record_optimized_param(optimized_dict)
        return optimized_dict
        
        