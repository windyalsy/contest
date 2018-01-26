import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import matplotlib.pylab as plt
import pickle
import os
from sklearn.externals import joblib




if __name__ == "__main__":

    modelName = "category1"
    modelPath = "../model/"
    modelFile = modelPath + modelName +'.pkl'
    with open(modelFile,'rb') as file:
        rf = joblib.load(file)

    featureFile = "../train_feature/e5e3cd1a03fee6bd.csv"
    targetFile = "../train_clip_padding/e5e3cd1a03fee6bd.csv"
    feature = pd.read_csv(featureFile)
    target = (pd.read_csv(targetFile))['label']



    prediction_prob = rf.predict_proba(feature)[:,1]
    prediction = rf.predict(feature)
    precision = metrics.precision_score(target,prediction,pos_label=1,average='binary')
    recall = metrics.recall_score(target,prediction,pos_label=1,average='binary')
    f1score = metrics.f1_score(target,prediction,pos_label=1,average='binary')
    print("Precision:   %f"%precision)
    print("Recall   :   %f"%recall)
    print("F1score  :   %f"%f1score)
    print("AUC Score (Train): %f"% metrics.roc_auc_score(target,prediction_prob))


