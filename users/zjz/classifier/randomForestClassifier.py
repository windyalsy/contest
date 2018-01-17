import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import matplotlib.pylab as plt

def RFClassier(object):
    def __init__(self,featureFile,targetFile):
        self.feature = pd.read_csv(featureFile)
        self.target = (pd.read_csv(targetFile))['label']


if __name__ == "__main__":
    featureFile = "../train_feature/40e25005ff8992bd.csv"
    targetFile = "../train_clip_padding/40e25005ff8992bd.csv"
    feature = pd.read_csv(featureFile)
    target = (pd.read_csv(targetFile))['label']
    rf = RandomForestClassifier(oob_score=True,random_state=10)
    rf.fit(feature,target)

    featureFile = "../train_feature/71595dd7171f4540.csv"
    targetFile = "../train_clip_padding/71595dd7171f4540.csv"
    feature = pd.read_csv(featureFile)
    target = (pd.read_csv(targetFile))['label']
    prediction_prob = rf.predict_proba(feature)[:,1]
    prediction = rf.predict(feature)
    precision = metrics.precision_score(target,prediction,average='binary')
    recall = metrics.recall_score(target,prediction,average='binary')
    f1score = metrics.f1_score(target,prediction,average='binary')
    print("Precision:   %f"%precision)
    print("Recall   :   %f"%recall)
    print("F1score  :   %f"%f1score)
    print("AUC Score (Train): %f"% metrics.roc_auc_score(target,prediction_prob))
