import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import matplotlib.pylab as plt
from sklearn.externals import joblib
import os
import get_fretures

class RF(object):

    ''' Params  df
        df      :   Dataframe
                    'KPI ID','timestamp','value','label'
        modelName   : string 训练好模型存放名字，后缀.pkl
        modelPath   : string
        Returns analysis

        return  字段：["Precision","Recall","F1score","AUC Score"]
        '''
    def train(self,path,id,modelName,modelPath):
        df = get_fretures.inputDF(path,id)
        feature = get_fretures.getFeatures(id)
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

    ''' Params  df
        df      :   Dataframe
                    'KPI ID','timestamp','value','label'
        modelName   : string
        modelPath   : string
        Returns analysis

        return  字段：["Precision","Recall","F1score","AUC Score"]
        '''
    def test(self,path,id,modelName,modelPath):
        df = get_fretures.inputDF(path,id)
        feature = get_fretures.getFeatures(id)
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


    ''' Params  df
        df      :   Dataframe
                    'KPI ID','timestamp','value',
        modelName   : string
        modelPath   : string
        Returns predictDf

        return  Dataframe
                字段：'KPI ID','timestamp','predict'
        '''
    def run(self,path,id,modelName,modelPath):
        feature = get_fretures.getFeatures(id)
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
    rf = RF()
    # print(rf.train("../train_clip_padding/","40e25005ff8992bd.csv","category1","../model/"))
    # print(rf.test("../train_clip_padding/","e5e3cd1a03fee6bd.csv","category1","../model/"))
    print(rf.run("../test/","e5e3cd1a03fee6bd.csv","category1","../model/"))
