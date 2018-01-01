#encoding:utf-8

import csv


if __name__ == "__main__":
    c1 = open("/Users/hupeng/PycharmProjects/fix/file/e0770391decc44cemid1.csv", "rb")  # 以rb的方式打开csv文件
    read = csv.reader(c1)
    timelist = []
    valuelist = []
    labellist = []
    flaglist = []
    for line in read:
        timelist.append(line[1])
        valuelist.append(line[2])
        labellist.append(line[3])
        flaglist.append(line[4])
    c1.close()

    c2 = open("/Users/hupeng/PycharmProjects/fix/file/e0770391decc44cemid2.csv", "rb")  # 以rb的方式打开csv文件
    read = csv.reader(c2)
    timelist2 = []
    valuelist2 = []
    labellist2 = []
    for line in read:
        timelist2.append(line[1])
        valuelist2.append(line[2])
        labellist2.append(line[3])
    c2.close()

    i = 1
    # for i in range(i,timelist.__len__()):
    #     while(timelist[i] == timelist2[i] and flaglist[i] == 1):
    #         valuelist[i] = (int(valuelist[i])+int(valuelist2[i]))/2
    #         labellist[i] = labellist[i] or labellist2[i]

    c3 = open("/Users/hupeng/PycharmProjects/fix/file/e0770391decc44cefix.csv", "wb")
    writer = csv.writer(c3)
    for i in range(0, timelist.__len__()):

        rlist = []
        rlist.append("e0770391decc44ce")
        rlist.append(timelist[i])

        if (timelist[i] == timelist2[i] and int(flaglist[i]) == 1):
            valuenew = (float(valuelist[i]) + float(valuelist2[i])) / 2
            labelnew = labellist[i] or labellist2[i]

            rlist.append(valuenew)
            rlist.append(labelnew)
        else:
            rlist.append(valuelist[i])
            rlist.append(labellist[i])
        writer.writerow(rlist)
    c3.close()
    print "complete"


