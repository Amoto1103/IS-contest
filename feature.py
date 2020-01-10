import csv
import numpy as np
import ap
import os

class Host:
    def __init__(self,ip):
        self.ip=ip
        self.neighbour=set()
        self.flowBytes=[]
        self.maxFlowBytes=0

    def addData(self,ip,totLenFwdPkts,totLenBwdPkts):
        self.neighbour.add(ip)
        length = totLenFwdPkts + totLenBwdPkts
        if length:
            self.flowBytes.append(length)
        if length > self.maxFlowBytes:
            self.maxFlowBytes = length

def connect(hosts,c_list):
    temp = []
    for i in c_list:
        temp.append(len(hosts[i].neighbour))
    return np.max(temp)

def connect_check(hosts,c_list):
    temp = []
    thres = 100
    for i in range(len(c_list)):
        if len(hosts[c_list[i]].neighbour) > thres:
            temp.append(i)
    return temp

def neighbour(hosts,c_list):
    length = len(c_list)
    temp = []
    for i in range(length):
        for j in range(i):
            temp.append(len(hosts[c_list[i]].neighbour.intersection(hosts[c_list[j]].neighbour))//
                        len(hosts[c_list[i]].neighbour.union(hosts[c_list[j]].neighbour)))
    return np.max(temp)

def neighbour_check(hosts,c_list):
    length = len(c_list)
    temp = []
    thres = 0.2
    for i in range(length):
        for j in range(i):
            if (len(hosts[c_list[i]].neighbour.intersection(hosts[c_list[j]].neighbour))//
                len(hosts[c_list[i]].neighbour.union(hosts[c_list[j]].neighbour))) > thres:
                temp.append(i)
                temp.append(j)
    return temp

def hot(hosts,c_list):
    temp = []
    for i in c_list:
        if hosts[i].maxFlowBytes == 0:
            continue
        count = 0
        for length in hosts[i].flowBytes:
            if length > 0.8 * hosts[i].maxFlowBytes:
                count += 1
        temp.append(count)
    return np.min(temp)

def hot_check(hosts,c_list):
    temp = []
    thres = 10
    for i in range(len(c_list)):
        if hosts[c_list[i]].maxFlowBytes == 0:
            continue
        count = 0
        for length in hosts[c_list[i]].flowBytes:
            if length > 0.8 * hosts[c_list[i]].maxFlowBytes:
                count += 1
        if count < thres:
            temp.append(i)
    return temp

def main(name,index):
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
                    host.addData(row[3],int(row[10]),int(row[11]))
                    ctrl[0]=0
                
                elif row[3]==host.ip:
                    host.addData(row[1],int(row[11]),int(row[10]))
                    ctrl[1]=0
         
            if(ctrl[0]):
                newhost=Host(row[1])
                newhost.addData(row[3],int(row[10]),int(row[11]))
                hosts.append(newhost)
            if(ctrl[1]):
                newhost=Host(row[3])
                newhost.addData(row[1],int(row[11]),int(row[10]))
                hosts.append(newhost)
    
    c_list = ap.main(name)

    f = open('svm_in.txt', 'w')
    for clist in c_list:
        if len(clist) > 1:
            print('0 1:%s 2:%s 3:%s'%(str(connect(hosts,clist)),str(neighbour(hosts,clist)),str(hot(hosts,clist))),file=f)
    f.close()

    '''
    cmd="cd libsvm-3.23;./svm-predict ../svm-in.txt models/"+str(index)+".model ../svm-out.txt;cd .."
    os.system(cmd)
    
    '''

    f = open('svm_out.txt', 'r')
    svm = f.readlines()
    f.close()
    f = open('cluster.txt', 'r')
    clusters = f.readlines()
    f.close()
    f = open('output.txt', 'w')
    for clustersID in range(len(svm)):
        if svm[clustersID] == '1\n':
            num = -1
            for clist in c_list:
                if len(clist) > 1:
                    num += 1
                if num == clustersID:
                    break
            temp1 = set(connect_check(hosts,clist))
            temp2 = set(neighbour_check(hosts,clist))
            temp3 = set(hot_check(hosts,clist))
            temp = temp1.union(temp2).union(temp3)
            cluster = clusters[clustersID]
            ips = cluster[1:-2].split(sep=', ')
            for ipID in temp:
                print(ips[ipID][1:-1], file = f)
    f.close()


if __name__ == '__main__':
    main()
