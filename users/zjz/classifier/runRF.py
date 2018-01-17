import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import matplotlib.pylab as plt
from sklearn.externals import joblib
import os


if __name__ == "__main__":

    # name = "40e25005ff8992bd.csv"
    # featureFile = "../test_feature/"+name
    # targetFile = "../test/40e25005ff8992bd.csv"+name

    featureFile = "../test_feature/e5e3cd1a03fee6bd.csv"
    targetFile = "../test/e5e3cd1a03fee6bd.csv"
    name = os.path.basename(featureFile)
    predictPath = "../predict/"
    if not os.path.exists(predictPath):
        os.makedirs(predictPath)
    predictFile = predictPath + name
    feature = pd.read_csv(featureFile)
    target = pd.read_csv(targetFile)

    modelName = "category1"
    modelPath = "../model/"
    modelFile = modelPath + modelName +'.pkl'
    with open(modelFile,'rb') as file:
        rf = joblib.load(file)

    prediction_prob = rf.predict_proba(feature)[:,1]
    prediction = rf.predict(feature)
    label = pd.Series(prediction)
    target['predict'] = label
    predictDf = target.drop(['value'], axis=1)

    predictDf.to_csv(predictFile, index=False,columns=None)

