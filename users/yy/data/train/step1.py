import os
import csv
import pandas as pd

class Step1(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.fill(self.id_list)

    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def fill(self, id_list):
        for id in id_list:
            interval = self.getInterval(id)
            c = open("parts/"+id)
            reader = csv.DictReader(c)
            res = []
            front = {}
            for i, line in enumerate(reader):
                if i==0 :
                    res.append(line.copy())
                    front=line.copy()
                    continue
                time=(int(line["timestamp"])-int(front["timestamp"]))/interval
                if time>1 and time<=3:
                    zone=(float(line["value"])-float(front["value"]))/time
                    i=2
                    while(i<=int(time)):
                        front["timestamp"]=int(front["timestamp"])+interval
                        front["value"] = float(front["value"]) + zone
                        res.append(front.copy())
                        i+=1
                res.append(line.copy())
                front=line.copy()

            c.close()
            self.createFile("fill/step1_result/"+id,res)

    def getInterval(self,id):
        c = open("parts/" + id)
        reader = csv.DictReader(c)
        front=0
        last=0
        for i,line in enumerate(reader):
            print(line)
            if i==0:
                front=int(line["timestamp"])
            if i==1:
                last = int(line["timestamp"])
                break
        c.close()
        return last-front


    def createFile(self, path, list):
        df=pd.DataFrame(list)
        df.to_csv(path,index=False)

if __name__=='__main__':

    step1=Step1("parts")