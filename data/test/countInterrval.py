import pandas as pd
import os
import time

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
        amounts=[]
        starts=[]
        ends=[]
        for id in id_list:
            df=self.getDataframe(id)
            interval=self.getInterval(df)
            sub=self.getSub(interval,df)
            omit= self.getOmit(sub)
            omit_path = os.path.abspath(os.path.join(os.getcwd(), "omit", id))
            self.createFile(omit_path, omit)

            ids.append(id.split(".")[0])
            intervals.append(interval)
            omits.append(omit.size)
            start,end=self.getStartAndEnd(df)
            starts.append(start)
            ends.append(end)
            amounts.append(df.size)
        print(starts)
        self.createResult(ids,intervals,omits,amounts,starts,ends)


    def getInterval(self, df):
        t1 = int(df.iloc[3])
        t2 = int(df.iloc[4])
        return t2-t1

    def getDataframe(self, id):
        read_path = os.path.join(os.getcwd(), "parts", id)
        df = pd.read_csv(read_path)
        df1 = df["timestamp"]
        return df1

    def getSub(self, interval, df):
        df1 = df[0:1]-interval
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

    def createFile(self, path, df,columns=None):
        df.to_csv(path, index=False,columns=columns)

    def createResult(self, ids, intervals, omits,amounts,starts,ends):
        result=pd.DataFrame({"id":ids, "interrval":intervals, "omit": omits,"amount":amounts,"start":starts,"end":ends})
        columns = ['id', 'interrval', 'amount', 'omit','start','end']
        result_path = os.path.abspath(os.path.join(os.getcwd(), "result", "result.csv"))
        if os.path.isfile(result_path):
            os.remove(result_path)
        self.createFile(result_path,result,columns)

    def getStartAndEnd(self,df):
        start=df.get(0)
        end=df.get(df.size-1)
        timeArray = time.localtime(start)
        otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        timeArray = time.localtime(end)
        otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        return otherStyleTime1,otherStyleTime2




if __name__=='__main__':
    parts_path = os.path.abspath(os.path.join(os.getcwd(), "parts"))
    interval=Interval(parts_path)