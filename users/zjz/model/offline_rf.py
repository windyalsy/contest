import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import matplotlib.pylab as plt
from sklearn.externals import joblib
from sklearn.preprocessing import Imputer
import os
import get_fretures

class Offline_RF(object):

    ''' Params
        offlineFeaturesPath:    string
                离线特征存放路径
        id      :    string
                特征文件名
        Returns fetures

        return  各个模型特征拼接成的Dataframe
        '''
    def getOfflineFeatures(self,offlineFeaturesPath,id):

        list = os.listdir(offlineFeaturesPath)
        features= pd.DataFrame(columns=['KPI ID','timestamp'])
        for modelName in list:
            if os.path.isdir(os.path.join(offlineFeaturesPath,modelName)):
                featureFile = os.path.join(offlineFeaturesPath,modelName,id)
                if not os.path.exists(featureFile):
                    print("%s not found"%featureFile)
                    exit()
                print("load..%s"%featureFile)
                feat = pd.read_csv(featureFile)
                features = pd.merge(features,feat,how ="outer", on = ['KPI ID','timestamp'])
        print(features)
        features = features.drop('KPI ID',axis=1).drop('timestamp',axis = 1)
        # features.to_csv("features.csv",)
        #对missing values 进行填充
        imp = Imputer(missing_values="NaN",strategy = "mean",verbose=0,axis=0)
        imp.fit(features)
        impFeatures = imp.transform(features)
        impFeatures = pd.DataFrame(impFeatures,columns=features.axes[1])
        # impFeatures.to_csv("impFeatures.csv",)
        return impFeatures




    ''' Params
        offlineFeaturesPath:    string
                离线特征存放路径
        path    :   string
                data 存放路径
        id      :   string
                特征文件名
        modelName   : string 训练好模型存放名字，后缀.pkl
        modelPath   : string
        Returns analysis

        return  字段：["Precision","Recall","F1score","AUC Score"]
        '''
    def train(self,path,offlineFeaturesPath,id,modelName,modelPath):
        df = get_fretures.inputDF(path,id)
        feature = self.getOfflineFeatures(offlineFeaturesPath,id)
        print(df)
        target = df['label']
        #参数的搜索空间
        paramGrid = {
            # 'n_estimators':range(30,71,10),
            #  'max_depth':range(10,14,2),
             # 'min_samples_split':range(50,201,20),
             # 'min_samples_leaf':range(10,60,10),
             # 'max_features':range(3,11,2)
             }
        rf = RandomForestClassifier(oob_score=False,random_state=10)
        gridSearch = GridSearchCV(param_grid=paramGrid,estimator=rf,scoring='roc_auc',n_jobs=-1,cv=5,verbose=10)
        gridSearch.fit(feature,target)
        print(gridSearch.best_params_, gridSearch.best_score_,)

        # modelName = "category1"
        # modelPath = "../model/"
        if not os.path.exists(modelPath):
            os.makedirs(modelPath)
        modelFile = modelPath + modelName +'.pkl'
        with open(modelFile,'wb') as file:
            joblib.dump(gridSearch.best_estimator_,file)

        rf = gridSearch.best_estimator_
        prediction_prob = rf.predict_proba(feature)[:,1]
        prediction = rf.predict(feature)
        precision = metrics.precision_score(target,prediction,pos_label=1,average='binary')
        recall = metrics.recall_score(target,prediction,pos_label=1,average='binary')
        f1score = metrics.f1_score(target,prediction,pos_label=1,average='binary')

        print("Precision:   %f"%precision)
        print("Recall   :   %f"%recall)
        print("F1score  :   %f"%f1score)
        print("AUC Score (Train): %f"% metrics.roc_auc_score(target,prediction_prob))

        columns = ["Precision","Recall","F1score","AUC Score"]
        results = [[precision,recall,f1score,metrics.roc_auc_score(target,prediction_prob)]]
        return pd.DataFrame(data=results,columns=columns)

    ''' Params
        offlineFeaturesPath:    string
                离线特征存放路径
        path    :   string
                data 存放路径
        id      :   string
                特征文件名
        modelName   : string
        modelPath   : string
        Returns analysis

        return  字段：["Precision","Recall","F1score","AUC Score"]
        '''
    def test(self,path,offlineFeaturesPath,id,modelName,modelPath):
        df = get_fretures.inputDF(path,id)
        feature = self.getOfflineFeatures(offlineFeaturesPath,id)
        target = df['label']

        modelFile = modelPath + modelName +'.pkl'
        with open(modelFile,'rb') as file:
            rf = joblib.load(file)

        prediction_prob = rf.predict_proba(feature)[:,1]
        prediction = rf.predict(feature)
        precision = metrics.precision_score(target,prediction,pos_label=1,average='binary')
        recall = metrics.recall_score(target,prediction,pos_label=1,average='binary')
        f1score = metrics.f1_score(target,prediction,pos_label=1,average='binary')
        print("Precision:   %f"%precision)
        print("Recall   :   %f"%recall)
        print("F1score  :   %f"%f1score)
        print("AUC Score (Test): %f"% metrics.roc_auc_score(target,prediction_prob))

        columns = ["Precision","Recall","F1score","AUC Score"]
        results = [[precision,recall,f1score,metrics.roc_auc_score(target,prediction_prob)]]
        return pd.DataFrame(data=results,columns=columns)


    ''' Params
        offlineFeaturesPath:    string
                离线特征存放路径
        path    :   string
                data 存放路径
        id      :   string
                特征文件名
        modelName   : string
        modelPath   : string
        Returns predictDf

        return  Dataframe
                字段：'KPI ID','timestamp','predict'
        '''
    def run(self,path,offlineFeaturesPath,id,modelName,modelPath):
        feature = self.getOfflineFeatures(offlineFeaturesPath,id)
        target = get_fretures.inputDF(path,id)

        modelFile = modelPath + modelName +'.pkl'
        with open(modelFile,'rb') as file:
            rf = joblib.load(file)

        prediction = rf.predict(feature)
        label = pd.Series(prediction)
        # print(label)
        target['predict'] = label
        predictDf = target.drop(['value'], axis=1)
        return predictDf



if __name__ == "__main__":

    offlineFeaturesPath = "./offline_features/"
    path = "../data/train/parts_without_omits/"
    id = "8bef9af9a922e0b3.csv"
    modelName = id.split('.')[0]
    modelPath = "./rf/"
    rf = Offline_RF()

    rf.train(path=path,offlineFeaturesPath=offlineFeaturesPath,id=id,modelName=modelName,modelPath=modelPath)
    # rf.test(path=path,offlineFeaturesPath=offlineFeaturesPath,id=id,modelName=modelName,modelPath=modelPath)
    # (rf.run(path=path,offlineFeaturesPath=offlineFeaturesPath,id=id,modelName=modelName,modelPath=modelPath)).to_csv('predict.csv')

