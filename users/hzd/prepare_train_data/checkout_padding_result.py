# -*- coding: utf-8 -*-

import pandas as pd;
import numpy as np;
import os;

class Checkout(object):
    def __init__(self, read_base_dir, filename):
        self.__read_base_dir = read_base_dir
        self.__filename = filename
        self.__interval = 60
    
    def __read_from_file(self, filename):
        df = pd.read_csv(filename)
        timestamp = df["timestamp"]
        return timestamp
    
    def __find_omits(self, timestamp):
        first_one = timestamp.iloc[0] - self.__interval
        first_line = pd.Series(first_one)
        begin = pd.concat([first_line, timestamp[:-1]], ignore_index=True)
        df = pd.DataFrame({"begin": begin, "end": timestamp})
        df["sub"] = (df["end"] - df["begin"]) // self.__interval
        df = df[df["sub"] != 1]
        return df
        
    def checkout_omits(self):
        for filename in self.__filename:
            read_path = os.path.join(self.__read_base_dir, filename)
            timestamp = self.__read_from_file(read_path)
            df = self.__find_omits(timestamp)
            if df.size == 0:
                print("%s doesn't have any omits." % filename)
            else:
                print("%s have omits." % filename)
                print(df[:5])
    
if __name__ == "__main__":
    filename = np.array(["a40b1df87e3f1c87.csv", "cff6d3c01e6a6bfa.csv", "affb01ca2b4f0b45.csv", \
        "8bef9af9a922e0b3.csv", "71595dd7171f4540.csv", "7c189dd36f048a6c.csv"])
    root_dir = os.getcwd()
    for i in range(3):
        root_dir = os.path.abspath(os.path.dirname(root_dir))
    read_dir = os.path.abspath(os.path.join(root_dir, "data", "train", "parts_without_omits"))
    checkout = Checkout(read_base_dir=read_dir, filename=filename)
    checkout.checkout_omits()

