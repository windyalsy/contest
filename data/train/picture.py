import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime

class Picture(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.draw(self.id_list)



    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def draw(self, id_list):
        for id in id_list:
            df = self.getDataframe(id)
            start=df.index[0]
            start = start + datetime.timedelta(days=10)
            end= start + datetime.timedelta(days = 10)
            plt.figure()
            df.plot(title=id.split(".")[0],xlim=[start,end])
            plt.savefig("pictures/" + id.split(".")[0])
            plt.close()

    def getDataframe(self, id):
        df = pd.read_csv("parts/" + id)
        df["timestamp"]=pd.to_datetime(df["timestamp"]*1000000000)
        df.set_index("timestamp", inplace=True)
        df1 = df["value"]
        return df1



if __name__=='__main__':

    interval=Picture("parts")