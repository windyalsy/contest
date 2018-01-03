import pandas as pd
import os
import time

class Merge(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.merge(self.id_list,path)

    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def merge(self, id_list,path):
        first_df=self.getDataframe(id_list[0],path)
        count=1
        while(count<id_list.__len__()-1):
            df=self.getDataframe(id_list[count],path)
            frames = [first_df, df]
            first_df = pd.concat(frames, ignore_index=True)
            count+=1
        self.createFile("total_without_omits/train_without_omits.csv",first_df)


    def getDataframe(self, id,path):
        df = pd.read_csv(path + id)
        return df

    def createFile(self, path, df,columns=None):
        df.to_csv(path, index=False,columns=columns)


if __name__=='__main__':

    interval=Merge("parts_without_omits/")