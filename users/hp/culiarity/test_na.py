from nose.tools import eq_, raises
from users.hp.culiarity.pyculiarity import detect_ts, detect_vec
from unittest import TestCase
import pandas as pd
import os
import numpy as np



class TestNAs(TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.raw_data = pd.read_csv(os.path.join(self.path,
                                                 '../../../data/train/parts_without_omits/8bef9af9a922e0b3.csv'),
                                    usecols=['timestamp', 'value'])



    def test_handling_of_leading_trailing_nas(self):
        self.raw_data["timestamp"] = pd.to_datetime(self.raw_data["timestamp"] * 1000000000)
        length = len(self.raw_data) - 1
##        for i in list(range(1+length)):
#        for i in range(10,len(self.raw_data) - 1):
        for i in range(10):
            self.raw_data.set_value(i, 'value', np.nan)
        self.raw_data.set_value(length, 'value', np.nan)
        # print(self.raw_data)
        # print("+++++++++")
        results = detect_ts(self.raw_data, max_anoms=0.02,
                            direction='both', plot=False)
        print (len(results['anoms'].iloc[:,1]))
        #print results['anoms']
        print (results['anoms']['timestamp'].values)
        arrs = results['anoms']['timestamp'].values
        #timecolumn = results['anoms'].iloc[1]['timestamp'].values

        #pre = pd.concat([timecolumn],axis=1)

        save = pd.DataFrame({'anomstime':arrs})

        #save.to_csv("anoms/8bef9af9a922e0b3anoms.csv",encoding='utf-8')
        return save
        # c3 = open("C:\\Users\\pehu\\Downloads\\pyculiarity-master\\tests\\07927a9a18fa19aepoint.csv", "w")
        # writer = csv.writer(c3)
        # for i in range(0,245):
        #     writer.writerow(str(results['anoms'].iloc[i]['timestamp']))
        #     print str(results['anoms'].iloc[i]['timestamp'])
        # c3.close()

        #eq_(len(results['anoms'].columns), 2)
        #eq_(len(results['anoms'].iloc[:,1]),48)


    @raises(ValueError)
    def test_handling_of_middle_nas(self):
        self.raw_data.set_value(len(self.raw_data) / 2, 'value', np.nan)
        detect_ts(self.raw_data, max_anoms=0.02, direction='both')
