# READ ME
-----------------------------
### 一、数据预处理
* `prepare_train_data` 目录下的内容为数据预处理程序， 本人所负责的预处理数据：KPI ID = `a40b1df87e3f1c87.csv` `cff6d3c01e6a6bfa.csv` 
`affb01ca2b4f0b45.csv` `8bef9af9a922e0b3.csv` `71595dd7171f4540.csv` `7c189dd36f048a6c.csv`
* **omit_padding.py** 负责填补缺省值， 处理规则如下：<br>
    1. 如果连续缺省值的个数小于等于3， 取缺省位置的前后均值填补， 若前后两项有一项的label为1则填补值的label=1
    2. 如果连续缺省值的个数大于3， 取前一周期相同时刻与后一周期相同时刻的均值填补，若前后两项有一项的label为1则填补值的label=1
    3. 填补后的数据存放于`contest/train/data/parts_without_omits/KPI ID.csv`
* **checkout_padding_result.py** 负责校验填补后数据的正确性
