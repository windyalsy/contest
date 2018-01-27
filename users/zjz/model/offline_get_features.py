import pandas as pd
import multiprocessing
import os


# 引入已经写好的model,每个model是一个类
# import A_model
# import B_model
# import C_model
from diff import DIFF
from ma import MA
from ewma import EWMA


# 每个id对模型输入都是标准dataframe，字段名为'KPI ID','timestamp','value','label'
# path为数据源目录，id是对应id的文件
def inputDF(path,id):
    df = pd.read_csv(path+id)
    return df

def getModels():
    modelList=[]
    # modelList.append(A_model)
    # modelList.append(B_model)
    # modelList.append(C_model)
    modelList.append(DIFF())
    modelList.append(MA())
    modelList.append(EWMA())
    return modelList

def getFeatures(id):
    dataPath="../data/train/parts_without_omits/"
    offlineFeaturesPath = "./offline_features/"
    df=inputDF(dataPath,id)
    modelList=getModels()

    # 多进程运行model获得返回值
    # 每个model必须有一个getResultDF方法，传入一个df，返回一个df
    # 返回df具体字段和行数需要注释在model内
    for model in modelList:
        modelName = model.__class__.__name__.lower()
        modelPath = os.path.join(offlineFeaturesPath,modelName)
        print("start extract %s ..."%modelName)
        feat = model.getResultDF(df)
        feat = pd.concat([df[["KPI ID","timestamp"]],feat],axis=1)
        if not os.path.isdir(modelPath):
            os.mkdir(modelPath)
        feat.to_csv(os.path.join(modelPath,id),index=False,columns=None)
        # print(feat)


    return feat

if __name__ == "__main__":
    print(getFeatures("8bef9af9a922e0b3.csv"))