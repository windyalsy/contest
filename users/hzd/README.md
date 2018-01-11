# READ ME
-----------------------------
### 一、数据预处理
* `prepare_train_data` 目录下的内容为数据预处理程序， 本人所负责的预处理数据：KPI ID = `a40b1df87e3f1c87.csv` `cff6d3c01e6a6bfa.csv` 
`affb01ca2b4f0b45.csv` `8bef9af9a922e0b3.csv` `71595dd7171f4540.csv` `7c189dd36f048a6c.csv`
* **omit_padding.py** 负责填补缺省值， 处理规则如下：<br>
    * 如果连续缺省值的个数小于等于3， 取缺省位置的前后均值填补， 若前后两项有一项的label为1则填补值的label=1
    * 如果连续缺省值的个数大于3， 取前一周期相同时刻与后一周期相同时刻的均值填补，若前后两项有一项的label为1则填补值的label=1
    * 填补后的数据存放于`contest/train/data/parts_without_omits/KPI ID.csv`
* **checkout_padding_result.py** 负责校验填补后数据的正确性
-------------------------------------
### 二、周期型KPI异常检测模型
* `model/seasonal`目录下存放有lstm回归模型和自己实现的较为笨拙的grid search超参数调参方法。 `lstm_model.py`为栈式LSTM回归模型，基于tensorflow搭建，下面对超参数做简要解释：<br>
    * `input_size`： 网络输入层的大小（即输入维度） 
    * `output_size`： 网络输出层的大小（即输出维度） 
    * `batch_size`: 批大小
    * `lstm_hide_size`： 网络隐藏层大小（即每个隐藏层含有多少lstm cell）
    * `lstm_depth`： 栈式LSTM的深度（即网络含有`lstm_depth`层隐藏层）
    * `lstm_learning_rate`： 学习率
    * `lstm_time_step`： 每个LSTM单元按时间展开的深度（即使用前`lstm_time_step`个时间步的数据预测下一个时间步的数据）
    * `gradient_clipping`: 梯度削减阈值（梯度大于该阈值时进行削减，用于防止梯度爆炸）
    * `train_drop_out`: 丢弃率，即网络中前一层每个单元有`drop out`的概率不传输到下一层（增加网络数量，用于增强网络泛化能力）
* `model`目录下存放有两个trainer的用例，其中`lstm_single_trainer.py`直接使用lstm_model做训练，用于手工调参；`lstm_grid_trainer.py`使用lstm_grid_search网格搜索最优参数，并将最优参数存入json文件。<br>
**注意： 代码中涉及的目录名和文件路径在运行前需做更改**
