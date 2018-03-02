# -*- coding: utf-8 -*-

import pandas as pd;
import numpy as np;
import os;

class Padding(object):
    def __init__(self, read_base_dir, write_base_dir, filename):
        self.__read_base_dir = read_base_dir
        self.__write_base_dir = write_base_dir
        self.__file_name = filename
        self.__interval = 60
        self.__season = 60 * 60 * 24
    
    def __read_from_file(self, filename):
        df = pd.read_csv(filename)
        df["omit"] = 0
        return df
    
    
    def __write_to_file(self, df, filename):
        df.to_csv(filename, index=False, columns=["KPI ID", "timestamp", "value", "label", "omit"])
    
    
    def __find_last_season(self, index, last_time, df):
        # 前一周期的数据不存在
        if last_time < df.iloc[0]["timestamp"]:
            next_time = last_time + 2 * self.__season
            return self.__find_next_season(index, next_time, df)
        else:
            # 前一周期的数据一定不会是缺失点
            index_diff_num = self.__season // self.__interval
            print("last_season_time: %i return_time: %i" % \
                (last_time, df.iloc[index - index_diff_num + 1]["timestamp"]))
            return df.iloc[index - index_diff_num + 1]
    
    
    def __find_next_season(self, index, next_time, df):
        # 后一周期的数据不存在
        if next_time > df.iloc[df.shape[0]-1]["timestamp"]:
            last_time = next_time - 2 * self.__season
            return self.__find_last_season(index, last_time, df)
        else:
            i = index + 1
            while df.iloc[i]["timestamp"] < next_time :
                i += 1
            if df.iloc[i]["timestamp"] == next_time:
                return df.iloc[i]
            # 后一周期的数据恰好是缺失点, 则再往后找一个周期
            else:
                next_time += self.__season
                return self.__find_next_season(index, next_time, df)
        
        
    def __padding_omit(self, df):
        i = 0
        while i < (df.shape[0] - 1):
            print("iterations : %i" % i)
            diff_num = (df.iloc[i+1]["timestamp"] - df.iloc[i]["timestamp"]) // self.__interval
            if diff_num == 1:
                i += 1
                continue
            elif diff_num <= 4:
                ID = df.iloc[i]["KPI ID"]
                for j in range(1, diff_num):
                    timestamp = df.iloc[i]["timestamp"] + self.__interval
                    value = (df.iloc[i]["value"] + df.iloc[i+1]["value"]) / 2
                    label = 0
                    if df.iloc[i]["label"] == 1 or df.iloc[i+1]["label"] == 1:
                        label = 1
                    omit = 1
                    insertRow = pd.DataFrame([[ID, timestamp, value, label, omit]], 
                        columns=["KPI ID", "timestamp", "value", "label", "omit"])
                    above = df.iloc[:i+1]
                    below = df.iloc[i+1:]
                    df = pd.concat([above, insertRow, below], ignore_index=True)
                    i += 1
            else:
                ID = df.iloc[i]["KPI ID"]
                for j in range(1, diff_num):
                    timestamp = df.iloc[i]["timestamp"] + self.__interval
                    last_time = timestamp - self.__season
                    last_season = self.__find_last_season(i, last_time, df)
                    next_time = timestamp + self.__season
                    next_season = self.__find_next_season(i, next_time, df)
                    value = (last_season["value"] + next_season["value"]) / 2
                    label = 0
                    if last_season["label"] == 1 or next_season["label"] == 1:
                        label = 1
                    omit = 1
                    insertRow = pd.DataFrame([[ID, timestamp, value, label, omit]], 
                        columns=["KPI ID", "timestamp", "value", "label", "omit"])
                    above = df.iloc[:i+1]
                    below = df.iloc[i+1:]
                    df = pd.concat([above, insertRow, below], ignore_index=True)
                    i += 1
        return df
    
    def start_padding(self):
        for filename in self.__file_name:
            read_path = os.path.join(self.__read_base_dir, filename)
            df = self.__read_from_file(read_path)
            print("read data from : %s" % read_path)
            print("*" * 66)
            df = self.__padding_omit(df)
            print("*" * 66)
            print("padding finished.")
            write_path = os.path.join(self.__write_base_dir, filename)
            self.__write_to_file(df, write_path)
            print("*" * 66)
            print("write data to : %s" % write_path)
    
    
if __name__ == "__main__":
    filename = np.array(["a40b1df87e3f1c87.csv", "cff6d3c01e6a6bfa.csv", "affb01ca2b4f0b45.csv", \
        "8bef9af9a922e0b3.csv", "71595dd7171f4540.csv", "7c189dd36f048a6c.csv"])
    root_dir = os.getcwd()
    for i in range(3):
        root_dir = os.path.abspath(os.path.dirname(root_dir))
    read_dir = os.path.abspath(os.path.join(root_dir, "data", "test", "parts"))
    write_dir = os.path.abspath(os.path.join(root_dir, "data", "test", "parts_without_omits"))
    padding = Padding(read_base_dir=read_dir, write_base_dir=write_dir, filename=filename)
    padding.start_padding()

