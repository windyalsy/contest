#encoding:utf-8

import csv


if __name__ == "__main__":
    c = open("/Users/hupeng/PycharmProjects/fix/file/8c892e5525f3e491.csv", "rb")  # 以rb的方式打开csv文件
    read = csv.reader(c)
    i = 0
    timelist = []
    valuelist = []
    labellist = []
    flaglist = []
    for line in read:
        timelist.append(line[1])
        valuelist.append(line[2])
        labellist.append(line[3])
        flaglist.append(0)
    print timelist[1],valuelist[1],labellist[1]
    print timelist[timelist.__len__()-1],valuelist[timelist.__len__()-1],labellist[timelist.__len__()-1]
    c.close()

    timelist.reverse()
    valuelist.reverse()
    labellist.reverse()
    flaglist.reverse()
    timelist.insert(0,timelist[timelist.__len__()-1])
    valuelist.insert(0,valuelist[valuelist.__len__()-1])
    labellist.insert(0,labellist[labellist.__len__()-1])
    flaglist.insert(0,flaglist[flaglist.__len__()-1])
    timelist = timelist[:-1]
    valuelist = valuelist[:-1]
    labellist = labellist[:-1]
    flaglist = flaglist[:-1]

    # print timelist

    i2 = 1
    while(timelist[i2]>timelist[timelist.__len__()-1]):
        inter = int(timelist[i2])-int(timelist[i2+1])
        if(inter == 120):
            avevalue = (float(valuelist[i2])+float(valuelist[i2+1]))/2
            #print avevalue
            valuelist.insert(i2+1,avevalue)

            avelabel = labellist[i2] or labellist[i2+1]
            #print avelabel
            labellist.insert(i2+1,avelabel)

            avetime = (int(timelist[i2])+int(timelist[i2+1]))/2
            #print avetime
            timelist.insert(i2+1,avetime)
            flaglist.insert(i2+1,0)
            i2 += 1

        elif(inter == 180):
            avevalue1 = (float(valuelist[i2-1]) + float(valuelist[i2 + 1])) / 2
            avevalue2 = (float(valuelist[i2]) + float(valuelist[i2 + 2])) / 2
            # print avevalue
            valuelist.insert(i2 + 1, avevalue1)
            valuelist.insert(i2 + 2, avevalue2)

            avelabel1 = labellist[i2 -1] or labellist[i2 + 1]
            avelabel2 = labellist[i2] or labellist[i2 + 2]
            # print avelabel
            labellist.insert(i2 + 1, avelabel1)
            labellist.insert(i2 + 2,avelabel2)

            avetime1 = (int(timelist[i2 - 1]) + int(timelist[i2 + 1])) / 2
            avetime2 = (int(timelist[i2]) + int(timelist[i2 + 2])) / 2
            #print avetime1,avetime2
            timelist.insert(i2 + 1, avetime1)
            timelist.insert(i2 + 2,avetime2)
            flaglist.insert(i2 + 1, 0)
            flaglist.insert(i2 + 2, 0)
            i2 += 2
        else:
            minute = inter/60
            for m in range(1,minute):
                valuelist.insert(i2+m,valuelist[i2 - 1440+m])
                labellist.insert(i2+m,labellist[i2 -1440 +m])
                timelist.insert(i2+m,int(timelist[i2 - 1440+m])-86400)
                print int(timelist[i2 - 1440+m])-86400
                flaglist.insert(i2+m,1)
            i2 += minute -1
        i2 += 1
    print "+++++++" + str(timelist)

    print i2

    timelist.reverse()
    valuelist.reverse()
    labellist.reverse()
    flaglist.reverse()
    timelist.insert(0, timelist[timelist.__len__() - 1])
    valuelist.insert(0, valuelist[valuelist.__len__() - 1])
    labellist.insert(0, labellist[labellist.__len__() - 1])
    flaglist.insert(0, flaglist[flaglist.__len__() - 1])
    timelist = timelist[:-1]
    valuelist = valuelist[:-1]
    labellist = labellist[:-1]
    flaglist = flaglist[:-1]

    c3 = open("/Users/hupeng/PycharmProjects/fix/file/8c892e5525f3e491mid2.csv", "wb")
    writer = csv.writer(c3)
    for i in range(0,timelist.__len__()):
        rlist = []
        rlist.append("8c892e5525f3e491")
        rlist.append(timelist[i])
        rlist.append(valuelist[i])
        rlist.append(labellist[i])
        rlist.append(flaglist[i])
        writer.writerow(rlist)
    c3.close()
    print "complete"
