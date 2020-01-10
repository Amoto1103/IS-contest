#coding:utf-8
import csv
import numpy as np


class Host:
    def __init__(self,ip):
        self.ip=ip
        self.totFwdPkts=[]
        self.totLenFwdPkts=[]
        self.totBwdPkts=[]
        self.totLenBwdPkts=[]
        self.timeArrival=[]
        self.timeDiff=[]
    
   
    def addData(self,totFwdPkts,totLenFwdPkts,totBwdPkts,totLenBwdPkts):
        self.totFwdPkts.append(totFwdPkts)
        self.totLenFwdPkts.append(totLenFwdPkts)
        self.totBwdPkts.append(totBwdPkts)
        self.totLenBwdPkts.append(totLenBwdPkts)

    def addTime(self,timeArrival):
        self.timeinfo=timeArrival.split()
        self.date=self.timeinfo[0].split("/")
        self.time=self.timeinfo[1].split(":")
        if(self.timeinfo[2]=="AM"):
            self.timeArr=int(self.date[0])*24*36000+int(self.time[0])*3600+int(self.time[1])*60+int(self.time[2])
        else:
            self.timeArr=int(self.date[0])*24*36000+(int(self.time[0])+12)*3600+int(self.time[1])*60+int(self.time[2])
        self.timeArrival.append(self.timeArr)


    def calculate(self):
        self.FwdPktsMean=np.mean(self.totFwdPkts)
        self.FwdPktsStdDev=np.std(self.totFwdPkts)
        self.BwdPktsMean=np.mean(self.totBwdPkts)
        self.BwdPktsStdDev=np.std(self.totBwdPkts)
        self.LenFwdPktsMean=np.mean(self.totLenFwdPkts)
        self.LenFwdPktsStdDev=np.std(self.totLenFwdPkts)
        self.LenBwdPktsMean=np.mean(self.totLenBwdPkts)
        self.LenBwdPktsStdDev=np.std(self.totLenBwdPkts)
        self.timeArrival.sort()
        if(len(self.timeArrival)==1):
            self.timeDiff.append(0)
        else:
            for i in range(0,len(self.timeArrival)-1):
                self.timeDiff.append(self.timeArrival[i+1]-self.timeArrival[i])
        self.maxTimeDiff=np.max(self.timeDiff)
        self.minTimeDiff=np.min(self.timeDiff)
        self.medianTimeDiff=np.median(self.timeDiff)
        self.stdDevTimeDiff=np.std(self.timeDiff)

def iter_update_R(dataLen,R,A,S):
    lam = 0.5
    for i in range(dataLen):
        for k in range(dataLen):
            max1 = -1e10
            for j in range(dataLen):
                if j != k:
                    if A[i][j] + S[i][j] > max1:
                        max1 = A[i][j] + S[i][j]
            R[i][k] = (1 - lam) * (S[i][k] - max1) + lam * R[i][k]
    return R

def iter_update_A(dataLen,R,A):
    lam = 0.5
    old_a = 0
    for i in range(dataLen):
        for k in range(dataLen):
            old_a = A[i][k]
            if i == k:
                A[i][k] = 0
                for j in range(dataLen):
                    if j != k:
                        if R[j][k] > 0:
                            A[i][k] += R[j][k]
            else :
                A[i][k] = 0
                for j in range(dataLen):
                    if j != k and j != i:
                        if R[j][k] > 0:
                            A[i][k] += R[j][k]
                if R[k][k] + A[i][k] > 0:
                    A[i][k] = 0
            A[i][k] = (1 - lam) * A[i][k] + lam * old_a
    return A

def cal_cls_center(dataLen,simi,R,A):
    max_iter = 100
    curr_iter = 0
    max_comp = 30
    curr_comp = 0
    class_cen = []
    while True:
        R = iter_update_R(dataLen,R,A,simi)
        A = iter_update_A(dataLen,R,A)
        for k in range(dataLen):
            if R[k][k] + A[k][k] > 0:
                if k not in class_cen:
                    class_cen.append(k)
                else:
                    curr_comp += 1
        curr_iter += 1
        if curr_iter >= max_iter or curr_comp > max_comp:
            break
    return class_cen

def main(name):
    hosts=[]
    with open(name+'_Flow.csv', 'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
           
            if((row[2]=='80')|(row[4]=='80')):
                continue
            if((row[2]=='443')|(row[4]=='443')):
                continue
            if((row[5]!='17')&(row[5]!='6')):
                continue
            ctrl=[1,1]
            for host in hosts:
                
                if row[1]==host.ip:
                    host.addData(int(row[8]),int(row[10]),int(row[9]),int(row[11]))
                    host.addTime(row[6])
                    ctrl[0]=0
                
                elif row[3]==host.ip:
                    host.addData(int(row[9]),int(row[11]),int(row[8]),int(row[10]))
                    host.addTime(row[6])
                    ctrl[1]=0
         
            if(ctrl[0]):
                newhost=Host(row[1])
                newhost.addData(int(row[8]),int(row[10]),int(row[9]),int(row[11]))
                newhost.addTime(row[6])
                hosts.append(newhost)
            if(ctrl[1]):
                newhost=Host(row[3])
                newhost.addData(int(row[9]),int(row[11]),int(row[8]),int(row[10]))
                newhost.addTime(row[6])
                hosts.append(newhost)

        for host in hosts:
            host.calculate()
            # print(host.ip)
            # print(host.totFwdPkts)
            # print(host.totLenFwdPkts)
            # print(host.totBwdPkts)
            # print(host.totLenBwdPkts)
            # print(host.FwdPktsMean)
            # print(host.FwdPktsStdDev)
            # print(host.LenFwdPktsMean)
            # print(host.LenFwdPktsStdDev)
            # print(host.BwdPktsMean)
            # print(host.BwdPktsStdDev)
            # print(host.LenBwdPktsMean)
            # print(host.LenBwdPktsStdDev)
            # print(host.timeDiff)
            # print(host.maxTimeDiff)
            # print(host.minTimeDiff)
            # print(host.medianTimeDiff)
            # print(host.stdDevTimeDiff)
    
    dataLen = len(hosts)
    FwdPktsMean = []
    FwdPktsStdDev = []
    LenFwdPktsMean = []
    LenFwdPktsStdDev = []
    BwdPktsMean = []
    BwdPktsStdDev = []
    LenBwdPktsMean = []
    LenBwdPktsStdDev = []
    maxTimeDiff = []
    minTimeDiff = []
    medianTimeDiff = []
    stdDevTimeDiff = []
    for host in hosts:
        FwdPktsMean.append(host.FwdPktsMean)
        FwdPktsStdDev.append(host.FwdPktsStdDev)
        LenFwdPktsMean.append(host.LenFwdPktsMean)
        LenFwdPktsStdDev.append(host.LenFwdPktsStdDev)
        BwdPktsMean.append(host.BwdPktsMean)
        BwdPktsStdDev.append(host.BwdPktsStdDev)
        LenBwdPktsMean.append(host.LenBwdPktsMean)
        LenBwdPktsStdDev.append(host.LenBwdPktsStdDev)
        maxTimeDiff.append(host.maxTimeDiff)
        minTimeDiff.append(host.minTimeDiff)
        medianTimeDiff.append(host.medianTimeDiff)
        stdDevTimeDiff.append(host.stdDevTimeDiff)
    avgFwdPktsMean, diffFwdPktsMean = np.average(FwdPktsMean), np.max(FwdPktsMean)-np.min(FwdPktsMean)
    avgFwdPktsStdDev, diffFwdPktsStdDev = np.average(FwdPktsStdDev), np.max(FwdPktsStdDev)-np.min(FwdPktsStdDev)
    avgLenFwdPktsMean, diffLenFwdPktsMean = np.average(LenFwdPktsMean), np.max(LenFwdPktsMean)-np.min(LenFwdPktsMean)
    avgLenFwdPktsStdDev, diffLenFwdPktsStdDev = np.average(LenFwdPktsStdDev), np.max(LenFwdPktsStdDev)-np.min(LenFwdPktsStdDev)
    avgBwdPktsMean, diffBwdPktsMean = np.average(BwdPktsMean), np.max(BwdPktsMean)-np.min(BwdPktsMean)
    avgBwdPktsStdDev, diffBwdPktsStdDev = np.average(BwdPktsStdDev), np.max(BwdPktsStdDev)-np.min(BwdPktsStdDev)
    avgLenBwdPktsMean, diffLenBwdPktsMean = np.average(LenBwdPktsMean), np.max(LenBwdPktsMean)-np.min(LenBwdPktsMean)
    avgLenBwdPktsStdDev, diffLenBwdPktsStdDev = np.average(LenBwdPktsStdDev), np.max(LenBwdPktsStdDev)-np.min(LenBwdPktsStdDev)
    avgmaxTimeDiff, diffmaxTimeDiff = np.average(maxTimeDiff), np.max(maxTimeDiff)-np.min(maxTimeDiff)
    avgminTimeDiff, diffminTimeDiff = np.average(minTimeDiff), np.max(minTimeDiff)-np.min(minTimeDiff)
    avgmedianTimeDiff, diffmedianTimeDiff = np.average(medianTimeDiff), np.max(medianTimeDiff)-np.min(medianTimeDiff)
    avgstdDevTimeDiff, diffstdDevTimeDiff = np.average(stdDevTimeDiff), np.max(stdDevTimeDiff)-np.min(stdDevTimeDiff)
    for host in hosts:
        host.FwdPktsMean = (host.FwdPktsMean - avgFwdPktsMean) / diffFwdPktsMean
        host.FwdPktsStdDev = (host.FwdPktsStdDev - avgFwdPktsStdDev) / diffFwdPktsStdDev
        host.LenFwdPktsMean = (host.LenFwdPktsMean - avgLenFwdPktsMean) / diffLenFwdPktsMean
        host.LenFwdPktsStdDev = (host.LenFwdPktsStdDev - avgLenFwdPktsStdDev) / diffLenFwdPktsStdDev
        host.BwdPktsMean = (host.BwdPktsMean - avgBwdPktsMean) / diffBwdPktsMean
        host.BwdPktsStdDev = (host.BwdPktsStdDev - avgBwdPktsStdDev) / diffBwdPktsStdDev
        host.LenBwdPktsMean = (host.LenBwdPktsMean - avgLenBwdPktsMean) / diffLenBwdPktsMean
        host.LenBwdPktsStdDev = (host.LenBwdPktsStdDev - avgLenBwdPktsStdDev) / diffLenBwdPktsStdDev
        host.maxTimeDiff = (host.maxTimeDiff - avgmaxTimeDiff) / diffmaxTimeDiff
        host.minTimeDiff = (host.minTimeDiff - avgminTimeDiff) / diffminTimeDiff
        host.medianTimeDiff = (host.medianTimeDiff - avgmedianTimeDiff) / diffmedianTimeDiff
        host.stdDevTimeDiff = (host.stdDevTimeDiff - avgstdDevTimeDiff) / diffstdDevTimeDiff
    
    simi = [[0] * dataLen for i in range(dataLen)]
    temp = []
    for i in range(dataLen):
        for j in range(i):
            s = -np.sqrt((hosts[i].FwdPktsMean - hosts[j].FwdPktsMean) ** 2 + \
                        (hosts[i].FwdPktsStdDev - hosts[j].FwdPktsStdDev) ** 2 + \
                        (hosts[i].LenFwdPktsMean - hosts[j].LenFwdPktsMean) ** 2 + \
                        (hosts[i].LenFwdPktsStdDev - hosts[j].LenFwdPktsStdDev) ** 2 + \
                        (hosts[i].BwdPktsMean - hosts[j].BwdPktsMean) ** 2 + \
                        (hosts[i].BwdPktsStdDev - hosts[j].BwdPktsStdDev) ** 2 + \
                        (hosts[i].LenBwdPktsMean - hosts[j].LenBwdPktsMean) ** 2 + \
                        (hosts[i].LenBwdPktsStdDev - hosts[j].LenBwdPktsStdDev) ** 2 + \
                        (hosts[i].maxTimeDiff - hosts[j].maxTimeDiff) ** 2 + \
                        (hosts[i].minTimeDiff - hosts[j].minTimeDiff) ** 2 + \
                        (hosts[i].medianTimeDiff - hosts[j].medianTimeDiff) ** 2 + \
                        (hosts[i].stdDevTimeDiff - hosts[j].stdDevTimeDiff) ** 2)
            simi[i][j] = s
            simi[j][i] = s
            temp.append(s)
    # p = np.max(temp)
    # p = np.min(temp)
    p = np.median(temp)
    for i in range(dataLen):
        simi[i][i] = p
    
    
    R = [[0] * dataLen for i in range(dataLen)]
    A = [[0] * dataLen for i in range(dataLen)]

    class_cen = cal_cls_center(dataLen, simi, R, A)
    class_cen_ip = []
    for i in class_cen:
        class_cen_ip.append(hosts[i].ip)
    print(class_cen_ip)

    c_list = [[] for i in range(len(class_cen))]
    c_list_ip = [[] for i in range(len(class_cen))]
    for i in range(dataLen):
        simi[i][i] = 0
        temp = []
        for j in class_cen:
            temp.append(simi[i][j])
        c = temp.index(np.max(temp))
        c_list[c].append(i)
        c_list_ip[c].append(hosts[i].ip)
    print(c_list_ip)

    f = open('cluster.txt', 'w')
    for clist in c_list_ip:
        if len(clist) == 1:
            continue
        print(clist, file=f)
    f.close()
    
    return c_list


if __name__ == '__main__':
    main()
