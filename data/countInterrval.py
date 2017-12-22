import pandas as pd
import os

class Interval(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.classifyByInterval(self.id_list)



    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def classifyByInterval(self, id_list):
        ids=[]
        intervals=[]
        omits=[]
        for id in id_list:
            df=self.getDataframe(id)
            interval=self.getInterval(df)
            sub=self.getSub(interval,df)
            omit= self.getOmit(sub)
            self.createFile("omit/" + id + ".csv",omit)
            ids.append(id)
            intervals.append(interval)
            omits.append(omit.size)
        self.createResult(ids,intervals,omits)


    def getInterval(self, df):
        t1 = int(df[0:1])
        t2 = int(df[1:2])
        return t2-t1

    def getDataframe(self, id):
        df = pd.read_csv("parts/" + id)
        df1 = df["timestamp"]
        return df1

    def getSub(self, interval, df):
        df1 = df[0:1]-60
        df2=df[0:]
        frames=[df1,df2]
        df1=pd.concat(frames,ignore_index=True)
        df1=df1[:-1]
        df=pd.DataFrame({'end':df,'begin':df1})
        df["sub"]=(df["end"]-df["begin"])/interval
        return df

    def getOmit(self, df):
        df=df[df["sub"]>1.0]
        return df

    def createFile(self, path, df):
        df.to_csv(path, index=False)

    def createResult(self, ids, intervals, omits):
        result=pd.DataFrame({"id":ids, "interrval":intervals, "omit": omits})
        self.createFile("result/result.csv",result)




if __name__=='__main__':

    interval=Interval("parts")