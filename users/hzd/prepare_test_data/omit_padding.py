# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import csv

class Padding(object):
    def __init__(self, read_path, write_path, omit_result_df):
        self.__season = 60 * 60 * 24
        self.read_path = read_path
        self.write_path = write_path
        self.id_list = self.getFileNames(read_path)
        self.omit_result_df = omit_result_df

    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def getInterval(self,id):
        tmp_path = os.path.join(self.read_path, id)
        c = open(tmp_path)
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
        df["omit"] = 0
        return df


    def __write_to_file(self, df, filename):
        if os.path.isfile(filename):
            os.remove(filename)
        df.to_csv(filename, index=False, columns=["KPI ID", "timestamp", "value", "omit"])
    
    
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
        
        
    def __padding_omit(self,df,interval,id):
        i = 0
        while i < (df.shape[0] - 1):
            print("ID : {}  lines : {}".format(id, i))
            diff_num = (df.iloc[i+1]["timestamp"] - df.iloc[i]["timestamp"]) // interval
            if diff_num == 1:
                i += 1
                continue
            elif diff_num <= 4:
                ID = df.iloc[i]["KPI ID"]
                for j in range(1, diff_num):
                    timestamp = df.iloc[i]["timestamp"] + interval
                    value = (df.iloc[i]["value"] + df.iloc[i+1]["value"]) / 2
                    omit = 1
                    insertRow = pd.DataFrame([[ID, timestamp, value, omit]], 
                        columns=["KPI ID", "timestamp", "value", "omit"])
                    above = df.iloc[:i+1]
                    below = df.iloc[i+1:]
                    df = pd.concat([above, insertRow, below], ignore_index=True)
                    i += 1
            elif diff_num > 4:
                ID = df.iloc[i]["KPI ID"]
                for j in range(1, diff_num):
                    timestamp = df.iloc[i]["timestamp"] + interval
                    last_time = timestamp - self.__season
                    last_season = self.__find_last_season(i, last_time, df,interval)
                    next_time = timestamp + self.__season
                    next_season = self.__find_next_season(i, next_time, df,interval)
                    value = (last_season["value"] + next_season["value"]) / 2
                    omit = 1
                    insertRow = pd.DataFrame([[ID, timestamp, value, omit]], 
                        columns=["KPI ID", "timestamp", "value", "omit"])
                    above = df.iloc[:i+1]
                    below = df.iloc[i+1:]
                    df = pd.concat([above, insertRow, below], ignore_index=True)
                    i += 1
            else:
                print("*"*66)
                print("diff_num error! ID: {}  diff_num: {}".format(id, diff_num))
                print("*"*66)
                os.system("pause")
        return df
    
    def start_padding(self):
        padding_res_list = os.listdir(self.write_path)
        to_padding = True
        for id in self.id_list:
            read_path = os.path.join(self.read_path, id)
            df = self.__read_from_file(read_path)
            interval = int(df.iloc[5]["timestamp"] - df.iloc[4]["timestamp"])
            print("*" * 66)
            print("read data from : %s" % read_path)
            # Check if it has been padding
            for padding_id in padding_res_list:
                if id == padding_id:
                    to_padding = False
                else:
                    continue
            if to_padding:
                for i in range(self.omit_result_df.shape[0]):
                    if self.omit_result_df.iloc[i]["id"] == id.split(".")[0]:
                        break
                if self.omit_result_df.iloc[i]["omit"] == 0:
                    print("*" * 66)
                    print("KPI : {} has not any omits.".format(id))
                else:
                    df = self.__padding_omit(df,interval,id)
                    print("*" * 66)
                    print("KPI : {} padding finished.".format(id))
                write_path = os.path.join(self.write_path, id)
                self.__write_to_file(df, write_path)
            else:
                to_padding = True
                continue




if __name__ == "__main__":
    root_dir = os.getcwd()
    for i in range(3):
        root_dir = os.path.abspath(os.path.dirname(root_dir))
    read_dir = os.path.abspath(os.path.join(root_dir, "data", "test", "parts"))
    write_path = os.path.abspath(os.path.join(root_dir, "data", "test", "parts_without_omits"))
    omit_result_path = os.path.abspath(os.path.join(root_dir, "data", "test", "result", "result.csv"))
    omit_result_df = pd.read_csv(omit_result_path)
    padding = Padding(read_dir, write_path, omit_result_df)
    padding.start_padding()

