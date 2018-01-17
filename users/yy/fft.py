

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.datasets.samples_generator import make_blobs
#
#
#
# X, y = make_blobs(n_samples=1000, n_features=2, centers=[[-1,-1], [0,0], [1,1], [2,2]], cluster_std=[0.4, 0.2, 0.2, 0.2],
#                   random_state =9)
#
# print(X)
# print(y)
#
#
# from sklearn.cluster import KMeans
# y_pred = KMeans(n_clusters=2, random_state=9).fit_predict(X)
# print(y_pred)
#
#
# from sklearn import metrics
# score=metrics.calinski_harabaz_score(X, y_pred)
# print(score)

import pandas as pd
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from matplotlib.pyplot import plot, show

class UseKmeans(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.classifyByKmeans(path,self.id_list)

    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def classifyByKmeans(self, path,id_list):
        valueDic = {}
        for id in id_list:
            df = self.getDataframe(path,id)
            array=[]
            valueDic[id.split(".")[0]]=self.getArray(df)

        self.kmeans(valueDic)

    def getDataframe(self, path,id):
        df = pd.read_csv(path + id)
        time=df["timestamp"].min()
        time=(int(time/86400)+3)*86400
        df=df[df["timestamp"]>=time]
        df=df.head(3000)



        # if id.split(".")[0] in ("54e8a140f6237526","b3b2e6d1a791d63a"):
        #     print(df["value"])
        return df

    def getArray(self,df):
        return np.array(df["value"])

    def kmeans(self,valueDic):
        kmeans=KMeans(n_clusters=15,max_iter=10000)
        valueArray=[]
        for key,value in valueDic.items():
            wave=np.cos(value)
            transformed = np.fft.fft(wave)
            print(transformed)
            plot(transformed)
            show()
        # kmeans.fit(valueArray)
        #
        # labelDic={}
        # for key,value in valueDic.items():
        #     label=kmeans.predict([value])[0]
        #     array=labelDic.get(label)
        #     if array==None:
        #         array=[]
        #     array.append(key)
        #     labelDic[label]=array
        # print(labelDic)


    def createFile(self, path, df,columns=None):
        df.to_csv(path, index=False,columns=columns)

    def createResult(self, ids, intervals, omits,amounts,starts,ends):
        result=pd.DataFrame({"id":ids, "interrval":intervals, "omit": omits,"amount":amounts,"start":starts,"end":ends})
        columns = ['id', 'interrval', 'amount', 'omit','start','end']
        self.createFile("result/result.csv",result,columns)



if __name__=='__main__':

    useKmeans=UseKmeans("data/train/parts_without_omits/")