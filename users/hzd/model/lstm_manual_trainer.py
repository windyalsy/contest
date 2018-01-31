#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import tensorflow as tf
import os
from seasonal.lstm_model import LstmRegression

def read_from_file(filepath):
    df = pd.read_csv(filepath)
    raw_data = df["value"].values
    normalize = (raw_data - np.mean(raw_data)) / np.std(raw_data)
    return raw_data, normalize


def prepare_train_data(normalize, 
                       train_set_num, 
                       batch_size, 
                       time_step, 
                       input_size, 
                       output_size):
    """
        Prepare train data for LSTM model input.
        LSTM model requires the input X(feature) has the shape of [num_of_batch, batch_size, time_step, input_size]
        and requires the input Y(label) has the shape of [num_of_batch, batch_size, output_size]
        
        Details:
            Suppose the time series and lstm params are as follows:
                time series: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                batch_size: 3
                time_step: 2
                input_size: 1
                output_size: 1
            input_x = [[[[1], [2]], [[2], [3]], [3, 4]], [[[4], [5]], [[5], [6]], [[6], [7]]], [[[7], [8]], [[8], [9]], [[9], [10]]]]
            label_y = [[[3], [4], [5]], [[6], [7], [8]], [[9], [10], [11]]]
    """
    normalize = np.reshape(normalize, (-1, input_size))
    x_shape = (train_set_num, time_step, input_size)
    y_shape = (train_set_num, output_size)
    train_x = np.zeros(x_shape, dtype=float)
    train_y = np.zeros(y_shape, dtype=float)
    assert train_set_num + time_step <= normalize.shape[0], "Train set is too large."
    for i in range(train_set_num):
        train_x[i, 0:, 0:] = normalize[i: i+time_step, 0:]
        train_y[i, 0:] = normalize[i+time_step, 0:]
    # Shuffle train data
    train_x = np.reshape(train_x, (-1, time_step*input_size))
    train_y = np.reshape(train_y, (-1, output_size))
    shuffle_data = np.hstack((train_x, train_y))
    np.random.shuffle(shuffle_data)
    train_x = shuffle_data[0:, 0: time_step*input_size]
    train_y = shuffle_data[0:, time_step*input_size:]
    train_x = np.reshape(train_x, (-1, batch_size, time_step, input_size))
    train_y = np.reshape(train_y, (-1, batch_size, output_size))
    return train_x, train_y


def prepare_predict_data(normalize,
                         raw_data,
                         time_step, 
                         input_size, 
                         output_size):
    normalize = np.reshape(normalize, (-1, input_size))
    validate_y = np.reshape(raw_data[time_step:], (-1, output_size))
    x_shape = (validate_y.shape[0], time_step, input_size)
    validate_x = np.zeros(x_shape, dtype=float)
    for i in range(validate_y.shape[0]):
        validate_x[i, 0:, 0:] = normalize[i: i+time_step, 0:]
    return validate_x, validate_y


def evaluate_model(predict_result, validate_y, mean, std, threshold):
    # Denormalize
    predict_result = predict_result * std + mean
    count = 0.0
    assert predict_result.shape[0] == validate_y.shape[0], "Length of predict_result is not equal with validate_y."
    for i in range(predict_result.shape[0]):
        diff = abs(predict_result[i] - validate_y[i])
        if diff <= validate_y[i] * threshold:
            count += 1
    accuracy = count / predict_result.shape[0]
    print("*"*66)
    print("LSTM Accuracy: %f" % accuracy)
    print("*"*66)

    
def main():
    """
        Define LSTM Model Params
    """
    input_size = 1
    output_size = 1
    batch_size = 200
    lstm_hide_size = 256
    lstm_depth = 5
    lstm_learning_rate = 6e-3
    lstm_time_step = 15
    gradient_clipping = 5
    train_drop_out = 0.5
    train_pass_num = 2000
    
    """
        Read Data From File
    """
    current_path = os.getcwd()
    filepath = os.path.join(current_path, "8bef9af9a922e0b3.csv")
    model_path = os.path.join(current_path, "lstm-model", "8bef9af9a922e0b3")
    load_path = os.path.join(current_path, "lstm-model")
    raw_data, normalize = read_from_file(filepath)
    mean = np.mean(raw_data)
    std = np.std(raw_data)
    # Ensure train_x can be partition into shape [num_of_batch, batch_size, time_step, input_size]
    train_set_num = normalize.shape[0] - lstm_time_step
    train_set_num = train_set_num - (train_set_num % (batch_size * lstm_time_step * input_size))
    train_x, train_y = prepare_train_data(normalize=normalize, 
                                          train_set_num=train_set_num, 
                                          batch_size=batch_size, 
                                          time_step=lstm_time_step, 
                                          input_size=input_size, 
                                          output_size=output_size)
    
    """
        Initialize LSTM Model Graph
    """
    lstm = LstmRegression(input_size=input_size,
                          output_size=output_size,
                          batch_size=batch_size,
                          lstm_hide_size=lstm_hide_size,
                          lstm_depth=lstm_depth,
                          lstm_learning_rate=lstm_learning_rate,
                          lstm_time_step=lstm_time_step,
                          gradient_clipping=gradient_clipping,
                          train_drop_out=train_drop_out)
    
    """
        LSTM Train
    """
    lstm.lstm_train(train_x, train_y, train_pass_num, model_path, 1)
    
    """
        Initialize LSTM Predict Graph
    """
    lstm_predict = LstmRegression(input_size=input_size,
                                  output_size=output_size,
                                  batch_size=1,
                                  lstm_hide_size=lstm_hide_size,
                                  lstm_depth=lstm_depth,
                                  lstm_learning_rate=lstm_learning_rate,
                                  lstm_time_step=lstm_time_step,
                                  gradient_clipping=gradient_clipping,
                                  train_drop_out=train_drop_out)
    """
        Evaluate LSTM Model
    """
    lstm_checkpoint = tf.train.latest_checkpoint(load_path)
    print(lstm_checkpoint)
    lstm_predict.load_model(lstm_checkpoint)
    validate_x, validate_y = prepare_predict_data(normalize=normalize,
                                                  raw_data=raw_data,
                                                  time_step=lstm_time_step, 
                                                  input_size=input_size, 
                                                  output_size=output_size)
    predict_result = lstm_predict.lstm_predict(validate_x)
    evaluate_model(predict_result, validate_y, mean, std, 0.10)
    
    
if __name__ == "__main__":
    main()
    
