import pandas as pd
import multiprocessing


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
    path="../train_clip_padding/"
    df=inputDF(path,id)
    modelList=getModels()
    features= pd.DataFrame()

    # modelList是一个产出特征值的model的集合
    pool = multiprocessing.Pool(processes=8)  # 创建8个进程
    results = []

    # 多进程运行model获得返回值
    # 每个model必须有一个getResultDF方法，传入一个df，返回一个df
    # 返回df具体字段和行数需要注释在model内
    for model in modelList:
        results.append(pool.apply(model.getResultDF, (df,)))
    pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join()  # 等待进程池中的所有进程执行完毕


    for res in results:
        features = pd.concat([features,res],axis=1)

    return features

if __name__ == "__main__":
    print(getFeatures("40e25005ff8992bd.csv"))