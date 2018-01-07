import pandas as pd
import os

class Step2(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.classifyByInterval(path,self.id_list)


    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def classifyByInterval(self, path,id_list):

        for id in id_list:
            df=self.getDataframe(path,id)
            interval=self.getInterval(df)
            start, end = self.getStartAndEnd(df)
            res=self.fill(df,start,end,interval)
            res=res.sort_values(by="timestamp")
            self.createFile("fill/step2_result/"+id,res)


    def getInterval(self, df):
        t1 = int(df["timestamp"][0:1])
        t2 = int(df["timestamp"][1:2])
        return t2-t1

    def getDataframe(self, path,id):
        df = pd.read_csv(path + id)
        return df


    def createFile(self, path, df,columns=None):
        df.to_csv(path, index=False,columns=columns)

    def getStartAndEnd(self,df):
        df1=df["timestamp"]
        start=df1.get(0)
        end=df1.get(df1.size-1)
        return int(start),int(end)


    def fill(self,df,start,end,interval):
        begin=start
        res=df.copy()
        count=0
        while(start<end):
            if(df[df["timestamp"]==start].__len__()==0):
                forward=start+86400
                backward=start-86400
                flag=0
                while(forward<end and flag==0):
                    omit=df[df["timestamp"]==forward]
                    if(omit.__len__()==1):
                        omit["timestamp"]=start
                        frames = [res, omit]
                        res = pd.concat(frames, ignore_index=True)
                        flag=1
                        count += 1
                        break
                    forward+=86400
                while (backward>begin and flag==0):
                    omit = df[df["timestamp"] == backward]
                    if (omit.__len__() == 1):
                        omit["timestamp"] = start
                        frames = [res, omit]
                        res = pd.concat(frames, ignore_index=True)
                        count += 1
                        break
                    backward -= 86400
            start+=interval
        print(count)
        return res


if __name__=='__main__':

    interval=Step2("fill/step1_result/")