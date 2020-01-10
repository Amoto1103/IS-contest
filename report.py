import sys
from report_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import time

class father_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):                           #构造函数
        super(father_window, self).__init__()
        self.setupUi(self)
        self.pushButton.setIcon(QtGui.QIcon("./picture/plotsuolue.png"))
        self.textBrowser.setText("2019_01_12_00_01_52.pcap")
        localtime=time.asctime(time.localtime(time.time()))
        self.textBrowser_2.setText(str(localtime))
        with open('tongji.txt',encoding='gbk',mode='r') as f:
            data = f.readlines()
            for a in data:
                self.listWidget.addItem(a)
        self.textBrowser_3.setText("10.16.1.155:52655\n10.16.168.58:49172\n10.16.100.102:50392\n10.1.11.84:63758\n10.1.2.199:25\n10.16.1.10:51513\n10.16.1.74:56182\n10.16.100.103:23575\n10.1.11.26:55698")
        self.textBrowser_4.setText("202.120.223.181\n23.228.226.66\n223.104.246.123\n202.120.223.44\n202.120.223.181\n111.206.52.98\n216.250.99.51\n202.120.217.170\n47.110.190.245")

    def show1(self):
        os.system("eog ./picture/plot.png")
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = father_window()
    ex.show()
    sys.exit(app.exec_())
