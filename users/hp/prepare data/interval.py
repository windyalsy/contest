#encoding:utf-8

import csv


if __name__ == "__main__":
    c = open("/Users/hupeng/PycharmProjects/fix/file/8c892e5525f3e491.csv", "rb")  # 以rb的方式打开csv文件
    read = csv.reader(c)
    i = 0
    timelist = []
    valuelist = []
    for line in read:
        timelist.append(line[1])
        valuelist.append(line[2])
    print timelist[0]
#    print timelist[147024]
    interlist = []
    indexlist = []
    troublelist = []
    for i in range(1,147023):
        inter = int(timelist[i+1])- int(timelist[i])
        if inter > 60:
            indexlist.append(i)
            interlist.append(inter/60-1)
            troublelist.append(timelist[i])
        else:
            continue

    c2 = open("/Users/hupeng/PycharmProjects/fix/file/test13.csv", "wb")
    writer = csv.writer(c2)
    for i in range(0, indexlist.__len__()):
        rlist = []
        rlist.append(indexlist[i])
        rlist.append(interlist[i])
        rlist.append(troublelist[i])
        writer.writerow(rlist)
    c2.close()
    print "complete"