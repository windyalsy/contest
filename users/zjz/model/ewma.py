import pandas as pd
import numpy as np
import os

FEATURENUM = 5
COULUMS = ['alpha01EWMA','alpha03EWMA','alpha05EWMA','alpha07EWMA','alpha09EWMA']


AlPHA01EWMA = 0
AlPHA03EWMA = 1
AlPHA05EWMA = 2
AlPHA07EWMA = 3
AlPHA09EWMA = 4

class EWMA(object):
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

        return  字段：['alpha01EWMA','alpha03EWMA','alpha05EWMA','alpha07EWMA','alpha09EWMA']
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
        Returns [alpha01EWMA,alpha03EWMA,alpha05EWMA,alpha07EWMA,alpha09EWMA]

        return EWMA with different alpha 0.1,0.3,0.5,0.7,0.9.
        '''
    def ewma(self,id):

        alpha01EWMA = 0
        alpha03EWMA = 0
        alpha05EWMA = 0
        alpha07EWMA = 0
        alpha09EWMA = 0


        if id == 0:
            alpha01EWMA = self.__value[id]
            alpha03EWMA = self.__value[id]
            alpha05EWMA = self.__value[id]
            alpha07EWMA = self.__value[id]
            alpha09EWMA = self.__value[id]

        if id == 1:
            alpha01EWMA = self.__value[id-1]
            alpha03EWMA = self.__value[id-1]
            alpha05EWMA = self.__value[id-1]
            alpha07EWMA = self.__value[id-1]
            alpha09EWMA = self.__value[id-1]

        if id > 1:
            alpha01EWMA = self.__value[id-1] * 0.1 + self.__feature[id-1,AlPHA01EWMA] * 0.9
            alpha03EWMA = self.__value[id-1] * 0.3 + self.__feature[id-1,AlPHA03EWMA] * 0.7
            alpha05EWMA = self.__value[id-1] * 0.5 + self.__feature[id-1,AlPHA05EWMA] * 0.5
            alpha07EWMA = self.__value[id-1] * 0.7 + self.__feature[id-1,AlPHA07EWMA] * 0.3
            alpha09EWMA = self.__value[id-1] * 0.9 + self.__feature[id-1,AlPHA09EWMA] * 0.1

        return[alpha01EWMA,alpha03EWMA,alpha05EWMA,alpha07EWMA,alpha09EWMA]


    def extract(self):
        for id in self.__value.index:
            self.__feature[id] = self.ewma(id)

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
        ewma = EWMA()
        print(ewma.getResultDF(df))
        print("finished !   "+outputPath+file)