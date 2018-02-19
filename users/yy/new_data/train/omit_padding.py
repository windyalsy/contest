# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import csv

class Padding(object):
    def __init__(self,path):
        self.__season = 60 * 60 * 24
        self.read_path=path
        self.id_list = self.getFileNames(path)

    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def getInterval(self,id):
        c = open(self.read_path + id)
        reader = csv.DictReader(c)
        front=0
        last=0
        for i,line in enumerate(reader):
            print(line)
            if i==2:
                front=int(line["timestamp"])
            if i==3:
                last = int(line["timestamp"])
                break
        c.close()
        return last-front
    
    def __read_from_file(self, filename):
        df = pd.read_csv(filename)
        return df


    def __write_to_file(self, df, filename):
        df.to_csv(filename, index=False)
    
    
    def __find_last_season(self, index, last_time, df,interval):
        # 前一周期的数据不存在
        if last_time < df.iloc[0]["timestamp"]:
            next_time = last_time + 2 * self.__season
            return self.__find_next_season(index, next_time, df,interval)
        else:
            # 前一周期的数据一定不会是缺失点
            index_diff_num = self.__season // interval
            print("last_season_time: %i return_time: %i" % \
                (last_time, df.iloc[index - index_diff_num + 1]["timestamp"]))
            return df.iloc[index - index_diff_num + 1]
    
    
    def __find_next_season(self, index, next_time, df,interval):
        # 后一周期的数据不存在
        if next_time > df.iloc[df.shape[0]-1]["timestamp"]:
            last_time = next_time - 2 * self.__season
            return self.__find_last_season(index, last_time, df,interval)
        else:
            i = index + 1
            while df.iloc[i]["timestamp"] < next_time :
                i += 1
            if df.iloc[i]["timestamp"] == next_time:
                return df.iloc[i]
            # 后一周期的数据恰好是缺失点, 则再往后找一个周期
            else:
                next_time += self.__season
                return self.__find_next_season(index, next_time, df,interval)
        
        
    def __padding_omit(self, df,interval):
        i = 0
        while i < (df.shape[0] - 1):
            print("iterations : %i" % i)
            diff_num = (df.iloc[i+1]["timestamp"] - df.iloc[i]["timestamp"]) // interval
            if diff_num == 1:
                i += 1
                continue
            elif diff_num <= 4:
                ID = df.iloc[i]["KPI ID"]
                for j in range(1, diff_num):
                    timestamp = df.iloc[i]["timestamp"] + interval
                    value = (df.iloc[i]["value"] + df.iloc[i+1]["value"]) / 2
                    label = 0
                    if df.iloc[i]["label"] == 1 or df.iloc[i+1]["label"] == 1:
                        label = 1
                    insertRow = pd.DataFrame([[ID, timestamp, value, label]], 
                        columns=["KPI ID", "timestamp", "value", "label"])
                    above = df.iloc[:i+1]
                    below = df.iloc[i+1:]
                    df = pd.concat([above, insertRow, below], ignore_index=True)
                    i += 1
            else:
                ID = df.iloc[i]["KPI ID"]
                for j in range(1, diff_num):
                    timestamp = df.iloc[i]["timestamp"] + interval
                    last_time = timestamp - self.__season
                    last_season = self.__find_last_season(i, last_time, df,interval)
                    next_time = timestamp + self.__season
                    next_season = self.__find_next_season(i, next_time, df,interval)
                    value = (last_season["value"] + next_season["value"]) / 2
                    label = 0
                    if last_season["label"] == 1 or next_season["label"] == 1:
                        label = 1
                    insertRow = pd.DataFrame([[ID, timestamp, value, label]], 
                        columns=["KPI ID", "timestamp", "value", "label"])
                    above = df.iloc[:i+1]
                    below = df.iloc[i+1:]
                    df = pd.concat([above, insertRow, below], ignore_index=True)
                    i += 1
        return df
    
    def start_padding(self):
        for id in self.id_list:
            interval = self.getInterval(id)
            df = self.__read_from_file(self.read_path+id)
            print("read data from : %s" % self.read_path+id)
            print("*" * 66)
            df = self.__padding_omit(df,interval)
            print("*" * 66)
            print("padding finished.")
            self.__write_to_file(df, "parts_without_omits/"+id)




if __name__ == "__main__":
    padding = Padding("parts/")
    padding.start_padding()

