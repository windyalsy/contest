import pandas as pd
import os
import numpy as np
from matplotlib.pyplot import plot, show
from matplotlib.pyplot import plot, show,bar


from numpy import asarray, ceil
import pandas
import rpy2.robjects.packages as packages
import rpy2.robjects as robjects

class UseSTL(object):

    def __init__(self, path):
        self.id_list=self.getFileNames(path)
        self.runSTL(path,self.id_list)

    def getFileNames(self,path):
        list = os.listdir(path)
        return list

    def runSTL(self, path,id_list):
        for id in id_list:
            if(id=="07927a9a18fa19ae.csv"):
                df = self.getDataframe(path,id)
                res = self.stl(df, 7,np=288)
                # bar(range(len(res["remainder"].head(200))), res["remainder"].head(200))
                plot(res["trend"])
                show()
                # print(res)
                self.createFile("model/stl_result/"+id,res,index=True)

    def getDataframe(self, path,id):
        df = pd.read_csv(path + id)
        # time=df["timestamp"].min()
        # time=(int(time/86400)+3)*86400
        # df=df[df["timestamp"]>=time]
        # df=df.head(12000)

        return df

    def getArray(self,df):
        return np.array(df["value"])

    def stl(self,df, ns, np=None):
        """
        Seasonal-Trend decomposition procedure based on LOESS

        data : pandas.Series

        ns : int
            Length of the seasonal smoother.
            The value of  ns should be an odd integer greater than or equal to 3.
            A value ns>6 is recommended. As ns  increases  the  values  of  the
            seasonal component at a given point in the seasonal cycle (e.g., January
            values of a monthly series with  a  yearly cycle) become smoother.

        np : int
            Period of the seasonal component.
            For example, if  the  time series is monthly with a yearly cycle, then
            np=12.
            If no value is given, then the period will be determined from the
            ``data`` timeseries.
        """
        # make sure that data doesn't start or end with nan
        df["timestamp"]=pd.to_datetime(df["timestamp"] * 1000000000)
        self.createFile("model/stl_result/ananomy" , df[df["label"] == 1], index=False)
        idx = df["timestamp"]
        data = df["value"]
        data.index = idx
        _data = data.copy()

        ts_ = robjects.r['ts']
        stl_ = robjects.r['stl']

        if isinstance(data.index[0], int):
            start = int(data.index[0])
        else:
            start = robjects.IntVector([data.index[0].year, data.index[0].month])

        ts = ts_(robjects.FloatVector(asarray(data)), start=start, frequency=np)

        result = stl_(ts, "periodic", robust=True)

        res_ts = asarray(result[0])
        try:
            res_ts = pandas.DataFrame({"seasonal": pandas.Series(res_ts[:, 0],
                                                                 index=data.index),
                                       "trend": pandas.Series(res_ts[:, 1],
                                                              index=data.index),
                                       "remainder": pandas.Series(res_ts[:, 2],
                                                                  index=data.index)})
        except:
            return res_ts, data

        return res_ts

    # def stl(self,df, ns, np=None, nt=None, nl=None, isdeg=0, itdeg=1, ildeg=1,
    #         nsjump=None, ntjump=None, nljump=None, ni=2, no=0, fulloutput=False):
    #     idx = pd.to_datetime(df["timestamp"]*1000000000)
    #     data = df["value"]
    #     data.index = idx
    #     _data = data.copy()
    #     # # TODO: account for non-monthly series
    #     # _idx = pandas.date_range(start=_data.index[0], end=_data.index[-1],
    #     #                          offset=pandas.datetools.MonthBegin())
    #     # data = pandas.Series(index=_idx)
    #     # data[_data.index] = _data
    #
    #     # zoo package contains na.approx
    #     zoo_ = packages.importr("zoo")
    #
    #     ts_ = robjects.r['ts']
    #     stl_ = robjects.r['stl']
    #     naaction_ = robjects.r['na.approx']
    #
    #     # find out the period of the time series
    #     if np is None:
    #         np = 12
    #
    #     if nt is None:
    #         nt = ceil((1.5 * np) / (1 - (1.5 / ns)))
    #     nt = nt + 1 if nt % 2 == 0 else nt
    #
    #     if nl is None:
    #         nl = np if np % 2 is 1 else np + 1
    #     if nsjump is None:
    #         nsjump = ceil(ns / 10.)
    #     if ntjump is None:
    #         ntjump = ceil(nt / 10.)
    #     if nljump is None:
    #         nljump = ceil(nl / 10.)
    #
    #     # convert data to R object
    #     # if np is 12:
    #     start = robjects.IntVector([data.index[0].year, data.index[0].month])
    #     ts = ts_(robjects.FloatVector(asarray(data)), start=start, frequency=np)
    #
    #     if nt is None:
    #         nt = robjects.rinterface.R_NilValue
    #
    #     result = stl_(ts, ns, isdeg, nt, itdeg, nl, ildeg, nsjump, ntjump, nljump,
    #                   False, ni, no, naaction_)
    #
    #     res_ts = asarray(result[0])
    #     try:
    #         res_ts = pandas.DataFrame({"seasonal": pandas.Series(res_ts[:, 0],
    #                                                              index=data.index),
    #                                    "trend": pandas.Series(res_ts[:, 1],
    #                                                           index=data.index),
    #                                    "remainder": pandas.Series(res_ts[:, 2],
    #                                                               index=data.index)})
    #     except:
    #         return res_ts, data
    #         raise
    #         #        res_ts = pandas.DataFrame({"seasonal" : pandas.Series(index=data.index),
    #         #                                   "trend" : pandas.Series(index=data.index),
    #         #                                   "remainder" : pandas.Series(index=data.index)})
    #
    #     if fulloutput:
    #         return {"time.series": res_ts,
    #                 "weights": result[1],
    #                 "call": result[2],
    #                 "win": result[3],
    #                 "deg": result[4],
    #                 "jump": result[5],
    #                 "ni": result[6],
    #                 "no": result[7]}
    #     else:
    #         return res_ts



    def createFile(self, path, df,index=False,columns=None):
        df.to_csv(path, index=index,columns=columns)





if __name__=='__main__':

    useSTL=UseSTL("data/train/parts_without_omits/")