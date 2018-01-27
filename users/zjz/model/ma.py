import pandas as pd
import numpy as np
import os

FEATURENUM = 10
COULUMS = ['win10MA','win20MA','win30MA','win40MA','win50MA',
           'win10MADiff','win20MADiff','win30MADiff','win40MADiff','win50MADiff']
WIN10MA = 0
WIN20MA = 1
WIN30MA = 2
WIN40MA = 3
WIN50MA = 4

WIN10MADIFF = 5
WIN20MADIFF = 6
WIN30MADIFF = 7
WIN40MADIFF = 8
WIN50MADIFF = 9


class MA(object):
    def __init__(self):
        self.__df= None
        self.__interval = None
        self.__value = None
        self.__feature = None
        self.__extra = None

    ''' Params  df
        df      :   Dataframe
                    'KPI ID','timestamp','value','label'
        Returns features

        return  字段：['win10MA','win20MA','win30MA','win40MA','win50MA',
                    'win10MADiff','win20MADiff','win30MADiff','win40MADiff','win50MADiff',]
                行数：同输入df行数
        '''
    def getResultDF(self,df):

        self.__df = df
        self.__interval = self.__df.iloc[1]['timestamp']-self.__df.iloc[0]['timestamp']
        self.__value = self.__df['value']
        self.__feature = np.zeros(shape=(len(self.__value.index),FEATURENUM))
        self.__extra = None
        features = self.extract()

        return features

    ''' Params  id
        id      :   int
                    id for rows
        Returns [win10MA,win20MA,win30MA,win40MA,win50MA,win10MADiff,win20MADiff,win30MADiff,win40MADiff,win50MADiff]

        return MA, MA diff,with different window.If window size less than assigned size, just average existing samples
        '''
    def ma(self,id):
        win10Start = id - 10
        win20Start = id - 20
        win30Start = id - 30
        win40Start = id - 40
        win50Start = id - 50

        win10MA = 0
        win20MA = 0
        win30MA = 0
        win40MA = 0
        win50MA = 0

        win10MADiff = 0
        win20MADiff = 0
        win30MADiff = 0
        win40MADiff = 0
        win50MADiff = 0

        if id == 0:
            win10MA = self.__value[id]
            win20MA = self.__value[id]
            win30MA = self.__value[id]
            win40MA = self.__value[id]
            win50MA = self.__value[id]
            return[win10MA,win20MA,win30MA,win40MA,win50MA,win10MADiff,win20MADiff,win30MADiff,win40MADiff,win50MADiff]

        if win10Start > 0:
            win10MA = self.__feature[id-1,WIN10MA]  + (self.__value[id - 1] -  self.__value[win10Start -1]) / 10.0
        else:
            for i in range(0,id):
                win10MA += self.__value[i]
            win10MA /= float(id)

        if win20Start > 0:
            win20MA = self.__feature[id-1,WIN20MA] + (self.__value[id - 1] -  self.__value[win20Start -1]) / 20.0
        else:
            for i in range(0,id):
                win20MA += self.__value[i]
            win20MA /= float(id)

        if win30Start > 0:
            win30MA = self.__feature[id-1,WIN30MA] + (self.__value[id - 1] -  self.__value[win30Start -1]) / 30.0
        else:
            for i in range(0,id):
                win30MA += self.__value[i]
            win30MA /= float(id)

        if win40Start > 0:
            win40MA = self.__feature[id-1,WIN40MA]  + (self.__value[id - 1] -  self.__value[win40Start -1]) / 40.0
        else:
            for i in range(0,id):
                win40MA += self.__value[i]
            win40MA /= float(id)

        if win50Start > 0:
            win50MA = self.__feature[id-1,WIN50MA] + (self.__value[id - 1] -  self.__value[win50Start -1]) / 50.0
        else:
            for i in range(0,id):
                win50MA += self.__value[i]
            win50MA /= float(id)

        win10MADiff = self.__value[id] - win10MA
        win20MADiff = self.__value[id] - win20MA
        win30MADiff = self.__value[id] - win30MA
        win40MADiff = self.__value[id] - win40MA
        win50MADiff = self.__value[id] - win50MA

        return[win10MA,win20MA,win30MA,win40MA,win50MA,win10MADiff,win20MADiff,win30MADiff,win40MADiff,win50MADiff]


    def extract(self):
        for id in self.__value.index:
            self.__feature[id] = self.ma(id)

        self.__extra = pd.DataFrame(data=self.__feature,columns=COULUMS)
        return self.__extra


if __name__ == "__main__":
    inputPath = '../train_clip_padding/'
    outputPath = '../train_feature/'
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    list = os.listdir(inputPath)
    for file in list:
        print("start extracting:    " +inputPath+file)
        df = pd.read_csv(inputPath+file)
        ma = MA()
        print(ma.getResultDF(df))
        print("finished !   "+outputPath+file)