#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import json
import codecs
import os
from seasonal.lstm_grid_search import LstmGridSearch

def read_from_file(filepath):
    df = pd.read_csv(filepath)
    raw_data = np.array(df["value"])
    normalize = (raw_data - np.mean(raw_data)) / np.std(raw_data)
    return raw_data, normalize


def main():
    """
        Read Data From File
    """
    current_path = os.getcwd()
    filepath = os.path.join(current_path, "8bef9af9a922e0b3.csv")
    model_path = os.path.join(current_path, "lstm-model-test", "8bef9af9a922e0b3")
    raw_data, normalize = read_from_file(filepath)
    param_path = os.path.join(current_path, "lstm-model-test", "lstm_param.json")
    param_dict = {  "input_size": 1,
                    "output_size": 1,
                    "batch_size": [100],
                    "lstm_hide_size": [256],
                    "lstm_depth": [5],
                    "lstm_learning_rate": [6e-3],
                    "lstm_time_step": [15],
                    "gradient_clipping": 5,
                    "train_drop_out": 0.5
        
                 }
    lstm_grid = LstmGridSearch(normalize_data=normalize,
                               train_set_num=1000,
                               param_path=param_path,
                               model_path=model_path,
                               param_dict=param_dict,
                               epoch=1)
    lstm_grid.grid_search()
    
    #Test read from param file
    with codecs.open(param_path, "r", encoding="utf-8") as f:
        params = json.load(f, encoding="utf-8")
        f.close()
        print(params)

if __name__ == "__main__":
    main()
    