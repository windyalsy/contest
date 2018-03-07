---
### Assignment 1
1. 处理数据：e5e3cd1a03fee6bd 40e25005ff8992bd
2. 此数据头部噪声过大，对预测无意义，直接去除开头部分数据

---
### Assignment 2
1. featureExtractor 提取特征，以文件形式存储
2. classfier 以文件形式记录特征，训练模型并保存

---
### Assignment 3
1. Team_model 按照约定接口实现各模型特征：DIFF、MA、EWMA
2. Team_model 按照约定接口实现随机森林的train，test，run
3. getFeatures中建议修改各模型返回特征Dataframe的拼接为contact

---
### Assignment 4
1. Team_model 改名model，增加文件夹data
2. model下增加离线特征提取offline_get_features、离线rf模型offline_rf
3. 在未调参的情况下： <br>
  Precision:   0.998066 <br>
  Recall   :   0.953789 <br>
  F1score  :   0.975425 <br>
  AUC Score (Train): 0.999999  <br>
  可能过拟合了
  
---
### Assignment 5
1. get_offline_features系列中对infinite数据置零
2. RF模型中，去除roc_auc度量，部分file计算结果不平衡。
3. util.py 提供remove padding等tool
