import sys
from myinterface import *
from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter
from tkinter.filedialog import askopenfilename
import os
import feature
import time
import _thread

class father_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):                           #构造函数
        super(father_window, self).__init__()
        self.setupUi(self)
        self.ctr_button4=0

    def p2p_static_analyse(self):
        #cmd="cd CICFlowMeter-4.0/bin;./cfm "+self.file+" ../.."
        #os.system(cmd)
        self.file="2019_01_12_00_01_52.pcap"
        i=self.comboBox.currentIndex()
        #feature.main(self.file,i)

    def p2p_dynamic_analyse(self):
        #cmd="cd CICFlowMeter-4.0/bin;./cfm "+self.file+" ../.."
        #os.system(cmd)
        #self.file="sample.pcap"
        #i=self.comboBox.currentIndex()
        #feature.main(self.file,i)

    def choose_pcap1(self):
        root=tkinter.Tk()
        root.withdraw()
        pcap_name=askopenfilename()
        root.destroy()
        self.file=pcap_name
        print (self.file)
        self.lineEdit_3.setText(pcap_name)

    def choose_pcap2(self):
        root=tkinter.Tk()
        root.withdraw()
        pcap_name=askopenfilename()
        root.destroy()
        self.file=pcap_name
        print (self.file)
        self.lineEdit_2.setText(pcap_name) 

    def choose_device(self):
        os.system("tcpdump -D > tmp.txt")
        with open('tmp.txt',encoding='gbk',mode='r') as f:
            data = f.readlines()
            for a in data:
                self.listWidget.addItem(a)
    
    def pool_static_analyse(self):
        cmd="./readnew "+self.file+" > log.txt"
        os.system(cmd)
        '''
        with open('log.txt',encoding='gbk',mode='r') as f:
            data = f.readlines()
            for a in data:
                print(a)
        '''
        time.sleep(3)
        #os.system("python3 report.py")
    
    def change_button4(self):
        #点了停止检测
        if(self.ctr_button4):
            self.pushButton_4.setText("开始检测")
            self.pushButton_4.setIcon(QtGui.QIcon(r'./picture/Start-icon.png'))
            self.ctr_button4=0
            _thread.start_new_thread(os.system,("python3 report2.py",))
            
        #点了开始检测
        else:
            self.pushButton_4.setText("停止检测")
            self.pushButton_4.setIcon(QtGui.QIcon(r'./picture/pause-icon.png'))
            self.ctr_button4=1
            _thread.start_new_thread(self.pool_dynamic_analyse,())

    def pool_dynamic_analyse(self):
        device_name=self.listWidget.currentItem().text()
        device_name1=device_name.split()
        device_name2=device_name1[0].split(".")[1]
        cmd="cd httpdump;./httpdump "+"-i "+device_name2
        os.system(cmd)


    def change_rule(self):
        cmd="gedit rule.txt"
        os.system(cmd)
        print(11)

    def changepage0(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def changepage1(self):
        self.stackedWidget.setCurrentIndex(1)

    def changepage3(self):
        self.stackedWidget.setCurrentIndex(3)

    def changepage4(self):
        self.stackedWidget.setCurrentIndex(4)


    def onclicked(self):
        item=self.treeWidget_2.currentItem()
        if(item.text(0)=='主页'):
            print(11111)
            self.stackedWidget.setCurrentIndex(2)
        elif(item.text(0)=='静态pcap包检测'):
            self.stackedWidget.setCurrentIndex(0)
        elif(item.text(0)=='动态流量检测'):
            self.stackedWidget.setCurrentIndex(3)
        elif(item.text(0)=='静态pcap包p2p检测'):
            self.stackedWidget.setCurrentIndex(4)
        elif(item.text(0)=='动态流量p2p成份检测'):
            self.stackedWidget.setCurrentIndex(1)

        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = father_window()
    ex.show()
    sys.exit(app.exec_())
