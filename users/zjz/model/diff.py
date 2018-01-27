import pandas as pd
import numpy as np
import os

FEATURENUM = 3
COULUMS = ['lastSlotDiff','lastDayDiff','lastWeekDiff']


class DIFF(object):

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

        return  字段：['lastSlotDiff','lastDayDiff','lastWeekDiff']
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
        Returns [lastSlotDiff,lastDayDiff,lastWeekDiff]

        return difference between current value and the value at the last slot, last day, as well as last week
        '''
    def diff(self,id):
        lastSlot = id - 1
        lastDay = id - int(24 * 60 * 60 / self.__interval)
        lastWeek =id - int(7 * 24 * 60 * 60 / self.__interval)

        if lastSlot > -1:
            lastSlotDiff = self.__value.iloc[lastSlot] - self.__value[id]
        else:
            # lastSlotDiff = np.NAN
            lastSlotDiff = 0

        if lastDay > -1:
            lastDayDiff = self.__value.iloc[lastDay] - self.__value[id]
        else:
            # lastDayDiff = np.NAN
            lastDayDiff = 0

        if lastWeek > -1:
            lastWeekDiff = self.__value.iloc[lastWeek] - self.__value[id]
        else:
            # lastWeekDiff = np.NAN
            lastWeekDiff = 0

        return[lastSlotDiff,lastDayDiff,lastWeekDiff]

    def extract(self):
        for id in self.__value.index:
            self.__feature[id] = self.diff(id)

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
        diff = DIFF()
        print(diff.getResultDF(df))
        print("finished !   "+outputPath+file)