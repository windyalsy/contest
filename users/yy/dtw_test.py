import pandas as pd
import os
import numpy as np
from dtw import dtw
import multiprocessing


def func(x_key, x_value,y_key, y_value):
    dist, cost, acc, path = dtw(x_value, y_value, dist=lambda x, y: abs(x - y))
    print(y_key + "  " + x_key + ":" + str(dist))
    return dist,x_key,y_key


class UseDTW(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.classifyByDTW(path,self.id_list)

    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def classifyByDTW(self, path,id_list):
        valueDic = {}
        for id in id_list:
                df = self.getDataframe(path,id)
                valueDic[id.split(".")[0]]=self.getArray(df)
        self.useDist(valueDic)


    def getDataframe(self, path,id):
        df = pd.read_csv(path + id)
        time=df["timestamp"].min()
        time=(int(time/86400)+5)*86400
        df=df[df["timestamp"]>=time]
        df=df.head(1000)


        # df["value"]=df["value"]/max(df["value"].max(),abs(df["value"].min()))
        df["value"] = df["value"]+abs(df["value"].min())
        # median=df["value"].median()
        # if median<0 :
        #     df["value"] = df["value"]+2*median
        # if median == 0:
        #     df["value"] = df["value"] + 1
        df["value"] = df["value"]/df["value"].median()


        return df

    def getArray(self,df):
        return np.array(df["value"])

    def createFile(self, path, df,columns=None):
        df.to_csv(path, index=False,columns=columns)

    def useDist(self,valueDic):
        resList=[]

        pool = multiprocessing.Pool(processes=8)  # 创建4个进程
        results = []


        for res in results:
            print(res.get())
        for x_key, x_value in valueDic.items():
            for y_key, y_value in valueDic.items():
                results.append(pool.apply_async(func, (x_key, x_value,y_key, y_value,)))
        pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        pool.join()  # 等待进程池中的所有进程执行完毕


        for res in results:

            dist=res.get()[0]
            x_key=res.get()[1]
            y_key=res.get()[2]
            x_set=set()
            y_set=set()
            for s in resList:
                if x_key in s:
                    x_set=s
                if y_key in s:
                    y_set=s
            if (x_set!=y_set or (len(x_set)==0 and len(y_set)==0)) and x_key!=y_key:
                print(y_key + "  " + x_key + ":" + str(dist) )
                if dist < 0.04:
                    if len(x_set) != 0 and len(y_set) != 0:
                        x_set=x_set.union(y_set)
                        resList.remove(y_set)
                    else:
                        if len(x_set) == 0 and len(y_set) != 0:
                            y_set.add(x_key)
                        if len(x_set) != 0 and len(y_set) == 0:
                            x_set.add(y_key)
                        if len(x_set)==0 and len(y_set)==0:
                            x_set.add(x_key)
                            y_set.add(y_key)
                            resList.append(x_set)
                            resList.append(y_set)

        print(resList)





                    # x_set=set()
                    # y_set=set()
                    # for s in resList:
                    #     if x_key in s:
                    #         x_set=s
                    #     if y_key in s:
                    #         y_set=s
                    # if (x_set!=y_set or (len(x_set)==0 and len(y_set)==0)) and x_key!=y_key:
                    #     dist, cost, acc, path = dtw(x_value, y_value, dist=lambda x, y: abs(x - y))
                    #     print(y_key + "  " + x_key + ":" + str(dist) )
                    #     if dist < 0.03:
                    #         if len(x_set) != 0 and len(y_set) != 0:
                    #             x_set=x_set.union(y_set)
                    #             resList.remove(y_set)
                    #         else:
                    #             if len(x_set) == 0 and len(y_set) != 0:
                    #                 y_set.add(x_key)
                    #             if len(x_set) != 0 and len(y_set) == 0:
                    #                 x_set.add(y_key)
                    #             if len(x_set)==0 and len(y_set)==0:
                    #                 x_set.add(x_key)
                    #                 y_set.add(y_key)
                    #                 resList.append(x_set)
                    #                 resList.append(y_set)








if __name__=='__main__':

    useDTW=UseDTW("data/train/parts_without_omits/")