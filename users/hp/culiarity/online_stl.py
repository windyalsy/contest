from nose.tools import eq_, raises
from users.hp.culiarity.pyculiarity import detect_ts, detect_vec
from unittest import TestCase
import pandas as pd
import os
import numpy as np
from users.hp.culiarity.test_na import TestNAs
from users.hp.culiarity.stl_test import UseSTL


class STL(object):

    def getResultDF(self,origindf):
        serdf = origindf.copy(1)
        path = "../../../data/train/parts_without_omits/"
        namestr = str(origindf["KPI ID"][1])
        print(namestr)
        na = TestNAs()
        na.setUp(path,namestr+".csv")
        anmosdf = na.test_handling_of_leading_trailing_nas()

        useSTL = UseSTL(path)
        df = useSTL.runSTL(origindf)
        anmostime = list(anmosdf["anomstime"].values)
        length = len(df)
        df.insert(0, "KPI ID", namestr)
        df.insert(5, "predict", 0)
        count = 0
        alltime = list(df["timestamp"].values)
        for i in range(length):
            if alltime[i] in anmostime:
                df.set_value(i, "predict", 1)
                count += 1
            else:
                continue
        df["timestamp"] = serdf["timestamp"]
        # df.to_csv("stl_result/" + id, index=False)

        print(count)
        print("complete")
        return df

# if __name__ == "__main__":
#     origindf = pd.read_csv("C://Users//pehu//Documents//contest//data//train//parts_without_omits//8bef9af9a922e0b3.csv")
#     stl = STL()
#     result = stl.getResultDF(origindf)
#     print(result)


