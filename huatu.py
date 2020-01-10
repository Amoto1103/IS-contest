import matplotlib.pyplot as plt


def plotdata():
    fin=open(r"./plotlog.txt",'r')
    plot=[]
    for line in fin.readlines():
        info=line.split()
        add1=1
        add2=1
        if(len(plot)==0):
            plot.append([info[0],int(info[2])])
            plot.append([info[1],int(info[2])])
        else:
            for i in range(0,len(plot)):
                if plot[i][0]==info[0]:
                    plot[i][1]+=int(info[2])
                    add1=0
                elif plot[i][0]==info[1]:
                    plot[i][1]+=int(info[2])
                    add2=0
            if(add1):
                plot.append([info[0],int(info[2])])                
            if(add2):
                plot.append([info[1],int(info[2])])
    #print(plot)
    fin.close()
    plot.sort(key=lambda data: data[1],reverse = True)
    maxNum=min(5,len(plot))
    x=[]
    y=[]
    for j in range(maxNum):
        x.append(plot[j][0])
        y.append(plot[j][1])
    plt.figure(figsize=(6,6.5))
    plt.bar(range(len(y)),y,width=0.7,color='rgb',tick_label=x)
    
    #plt.rcParams['font.sans-serif']=['SimHei'] 
    plt.title("Statistic Result (Top5)")
    
    plt.xlabel("IP Address")
    plt.ylabel("Number of Mining Packets")
    
    plt.xticks(range(len(x)),x,rotation=10)
    for k in range(len(x)):
        plt.text(k-0.1, y[k] + 0.05, y[k], fontsize=10)
    plt.savefig('./picture/plot.png')



    plt.figure(figsize=(3,3))
    plt.bar(range(len(y)),y,width=0.7,color='rgb',tick_label=x)
    plt.xticks([])
    plt.yticks([])
    #plt.rcParams['font.sans-serif']=['SimHei'] 

    plt.savefig('./picture/plotsuolue.png')
    #print(plot)

plotdata()
