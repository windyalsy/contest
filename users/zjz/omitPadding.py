import numpy as np
import pandas as pd
import os
import time

class Tools(object):


    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def getInterval(self,df):
        dfShift = df.copy()
        dfArray = np.array(df)
        dfShiftArray = np.array(dfShift)
        intervalArray = dfShiftArray[1:-1] - dfArray[0:-2]
        interval = intervalArray.min()
        return interval


    ''' Params  df
        df      :   Series
                    timestamp colom
        Returns [interval,omitDf,omitStatisticDf]
        interval:   int
        omitDf  :   Series
                    Index:timestamp,Value:interval between timestamp
        omitStatisticDf :Series
                    Some statistic information about omitDf '''
    def getOmitInfo(self,df):
        dfShift = df.copy()
        dfArray = np.array(df)
        dfShiftArray = np.array(dfShift)
        intervalArray = dfShiftArray[1:-1] - dfArray[0:-2]
        omitDf = pd.Series(intervalArray,index = dfArray[0:-2])
        omitStatisticDf = (omitDf.value_counts()).sort_index()
        interval = intervalArray.min()
        return [interval,omitDf,omitStatisticDf]

    def createFile(self, path, df,columns=None):
        df.to_csv(path, index=False,columns=columns)


    def findLastPeriod(self,df,period,point):
        for it in range(10):
            lastPointDf = df[df['timestamp'] ==point -it * period]
            if lastPointDf.shape[0] == 1 and lastPointDf.iloc[0]['value'] > 0:
                return lastPointDf.iloc[0]
        return None

    def findNextPeriod(self,df,period,point):
        for it in range(1,10):
            lastPointDf = df[df['timestamp'] ==point +it * period]
            if lastPointDf.shape[0] == 1 and lastPointDf.iloc[0]['value'] > 0:
                return lastPointDf.iloc[0]
        return None

    def omitPadding(self,df,period):
        dfTime = df['timestamp']
        tools = Tools()
        omitInfo = tools.getOmitInfo(dfTime)
        interval = omitInfo[0]
        #index represents timestamp,value represents omit interval
        omitDf = omitInfo[1]
        #index represents omit interval,value represents frequency
        omitStatisticDf = omitInfo[2]
        counter = 0
        for omitInterval in omitStatisticDf.index:
            count = int(omitInterval/interval)
            print(count)
            if count == 1:
                # #remove omit timestamps from omitDf
                # omitDf = omitDf[omitDf > omitInterval]
                continue

            #linear interpolation
            if count <= 4:
                omitPartDf = omitDf[omitDf == omitInterval]
                for point in omitPartDf.index:
                    counter += 1
                    leftIndex = (df[df['timestamp'] ==point].index)[0]
                    left = df.iloc[leftIndex]
                    right = df.iloc[leftIndex + 1]
                    insertRows = pd.DataFrame([left])
                    for it in range(1,count):
                        temp = left.copy()
                        temp['timestamp'] = point +  interval * it
                        temp['value'] = (left['value'] * it + right['value'] * (count - it)) / count
                        if right['label'] == 1:
                            temp['label'] = 1
                        # print (temp)
                        insertRows = insertRows.append(temp,ignore_index = True)

                    above = df.iloc[:leftIndex+1]
                    below = df.iloc[leftIndex+1:]
                    df = pd.concat([above, insertRows[1:], below], ignore_index=True)

            #borrow from other period
            if count > 4:
                omitPartDf = omitDf[omitDf == omitInterval]
                for point in omitPartDf.index:
                    counter += 1
                    leftIndex = df[df['timestamp'] ==point].index[0]
                    left = df.iloc[leftIndex]
                    right = df.iloc[leftIndex + 1]
                    insertRows = pd.DataFrame([left])
                    for it in range(1,count):
                        lastPoint = tools.findLastPeriod(df,period,point)
                        nextPoint = tools.findNextPeriod(df,period,point)
                        #if cannot find last period point, just use the left point to substitute
                        if lastPoint is None:
                            lastPoint = left
                        #if cannot find last period point, just use the left point to substitute
                        if nextPoint is None:
                            nextPoint = right

                        temp = lastPoint.copy()
                        temp['timestamp'] = point +  interval * it
                        temp['value'] = (lastPoint['value'] + nextPoint['value']) / 2
                        if lastPoint['label'] == 1:
                            temp['label'] = 1
                        # print (temp)
                        insertRows = insertRows.append(temp,ignore_index = True)

                    above = df.iloc[:leftIndex+1]
                    below = df.iloc[leftIndex+1:]
                    df = pd.concat([above, insertRows[1:], below], ignore_index=True)

        # print("Totally deals with %s missing intervals."%counter)
        return [df,omitInfo,counter]


# Clip dirty data in the head
class Clip(object):
    def __init__(self, path, timestamp=1496289600):
        self.__timestamp = timestamp
        self.__path = path

    def clip(self):
        list = os.listdir(self.__path)
        for file in list:
            df = pd.read_csv(self.__path+'/'+file)
            df = df[df['timestamp'] > self.__timestamp]
            df.to_csv(self.__path+'_clip/'+df.iloc[0] ['KPI ID']+'.csv', index=False,columns=None)


def startClipping():
    # clip records before certain timestamp
    path = "train"
    clip = Clip(path)
    clip.clip()

def startPadding():
    path = 'train_clip'
    list = os.listdir(path)
    for file in list:
        counter = 0
        tools = Tools()
        period = 24 * 60 * 60
        df = pd.read_csv(path+'/'+file)
        print("Starting processing %s "%file)
        [df,omitInfo,counter] = tools.omitPadding(df,period)
        print("%s Statistic Info:"%file)
        print(omitInfo[2])
        print("Totally deals with %s missing intervals."%counter)
        df.to_csv(path+'_padding/'+df.iloc[0] ['KPI ID']+'.csv', index=False,columns=None)

def startChecking():
    path = 'train_clip_padding'
    list = os.listdir(path)
    for file in list:
        tools = Tools()
        df = pd.read_csv(path+'/'+file)
        print("Starting checking %s "%file)
        omitInfo = tools.getOmitInfo(df['timestamp'])
        print("%s Statistic Info:"%file)
        print(omitInfo[2])


if __name__ =="__main__":

    startClipping()
    # startPadding()
    # startChecking()






