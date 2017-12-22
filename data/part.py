import pandas as pd

class PartData(object):

    def __init__(self, file):
        self.df=self.createDataftame(file)
        self.ids=self.getKPI_ID(self.df)
        self.separateFile(self.ids,self.df)

    def createDataftame(self,file):
        df=pd.read_csv(file)
        return df

    def getKPI_ID(self,df):
        ids=df["KPI ID"].drop_duplicates()
        return ids

    def separateFile(self,ids,df):
        for id in ids:
            df1=df[df["KPI ID"]==id]
            df2=df1.sort_values(["timestamp"])
            self.createFile(id,df2)


    def createFile(self,id,df):
        df.to_csv("parts/"+id+".csv",index=False)



if __name__=='__main__':

    part=PartData("train.csv")