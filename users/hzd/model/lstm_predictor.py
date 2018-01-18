#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import tensorflow as tf
import os
import json

class LstmPredictor(object):
    """
        Generate the feature for RF classifier.
        The feature is absolute value of the difference between predict value and real value.
        Attributes:
            self.__df: DataFrame which contains [KPI ID, timestep, value, label]
            self.__model_path: lstm model path
            self.__param_path: lstm param file path specified to file_name(.../.../param_file.json)
            self.__input_size: lstm model param
            self.__output_size: lstm model param
            self.__batch_size: lstm model param
            self.__lstm_hide_size: lstm model param
            self.__lstm_depth: lstm model param
            self.__lstm_learning_rate: lstm model param
            self.__lstm_time_step: lstm model param
            self.__lstm: LstmRegression object with specified params
            self.__real_val: real value
            self.__mean: mean of input data(for normalize and denormalize)
            self.__std: standard deviation of input data(for normalize and denormalize)
            self.__normalize: normalized data of input data(Z-score normalization)
            self.__predict_x: processed lstm input(shape is [num_of_features, time_step, input_size])
    """
    def __init__(self,
                 df,
                 model_path,
                 param_path):
        """
            Args:
                df: pandas.DataFrame which contains [KPI ID, timestep, value, label]
                model_path: lstm model path
                param_path: lstm param file path specified to file_name(.../.../param_file.json)
        """
        self.__df = df
        self.__model_path = model_path
        self.__param_path = param_path
        self.__init_model()
        self.__prepare_input()
        
    def __init_model(self):
        with open(self.__param_path, "r") as param_file:
            param = json.load(param_file)
        self.__input_size = param["input_size"]
        self.__output_size = param["output_size"]
        self.__batch_size = 1
        self.__lstm_hide_size = param["lstm_hide_size"]
        self.__lstm_depth = param["lstm_depth"]
        self.__lstm_learning_rate = param["lstm_learning_rate"]
        self.__lstm_time_step = param["lstm_time_step"]
        self.__lstm = LstmRegression(input_size=self.__input_size,
                                     output_size=self.__output_size,
                                     batch_size=self.__batch_size,
                                     lstm_hide_size=self.__lstm_hide_size,
                                     lstm_depth=self.__lstm_depth,
                                     lstm_learning_rate=self.__lstm_learning_rate,
                                     lstm_time_step=self.__lstm_time_step)
                                     
    def __prepare_input(self):
        """
            Prepare lstm input, make sure the shape of the input is [num_of_features, time_step, input_size].
            Cut off the first N(N=time_step) values.(Because lstm model uses N steps' value to predict the N+1 step)
        
        """
        raw_data = self.__df["value"].values
        raw_data = np.reshape(raw_data, (-1, self.__input_size))
        self.__real_val = raw_data[self.__lstm_time_step:]
        self.__mean = np.mean(raw_data, axis=0)
        self.__std = np.std(raw_data, axis=0)
        self.__normalize = (raw_data - self.__mean) / self.__std
        x_shape = (raw_data.shape[0]-self.__lstm_time_step, self.__lstm_time_step, self.__input_size)
        self.__predict_x = np.zeros(x_shape, dtype=float)
        for i in range(self.__predict_x.shape[0]):
            self.__predict_x[i, 0:, 0:] = self.__normalize[i: i+self.__lstm_time_step, 0:]
            
    def __get_predict_diff(self, real_val, predict_val):
        # Denormalize
        predict_val = predict_val * self.__std + self.__mean
        assert real_val.shape[0] == predict_val.shape[0], "The length of real_val is not equal with predict_val."
        # Flatten array
        predict_val = np.reshape(predict_val, (-1))
        real_val = np.reshape(real_val, (-1))
        diff = np.absolute(predict_val - real_val)
        return diff
        
    def get_feature(self):
        lstm_checkpoint = tf.train.latest_checkpoint(model_path)
        self.__lstm.load_model(lstm_checkpoint)
        predict_val = self.__lstm.lstm_predict(self.__predict_x)
        diff = self.__get_predict_diff(self.__real_val, predict_val)
        dict = {
                "lstm_feature": diff
               }
        fea_df = pd.DataFrame(dict)
        return fea_df
        
        