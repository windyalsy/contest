import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import matplotlib.pylab as plt
from sklearn.externals import joblib
import os

def RFClassier(object):
    def __init__(self,featureFile,targetFile):
        self.feature = pd.read_csv(featureFile)
        self.target = (pd.read_csv(targetFile))['label']


if __name__ == "__main__":

    featureFile = "../train_feature/40e25005ff8992bd.csv"
    targetFile = "../train_clip_padding/40e25005ff8992bd.csv"
    feature = pd.read_csv(featureFile)
    target = (pd.read_csv(targetFile))['label']

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

    modelName = "category1"
    modelPath = "../model/"
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
