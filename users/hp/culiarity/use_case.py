from users.hp.culiarity.test_na import TestNAs
from users.hp.culiarity.stl_test import UseSTL
import pandas as pd

if __name__ == "__main__":
    path = "../../../data/train/parts_without_omits/"
    id = "8bef9af9a922e0b3.csv"
    namestr = id[:-4]
    na = TestNAs()
    na.setUp(path,id)
    df2 = na.test_handling_of_leading_trailing_nas()

    useSTL = UseSTL(path)
    df = useSTL.runSTL(path,id)
    anmostime = list(df2["anomstime"].values)

    df3 = pd.read_csv(path + id)

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
    df["timestamp"] = df3["timestamp"]
    df.to_csv("stl_result/" + id, index=False)

    print(count)
    print("complete")