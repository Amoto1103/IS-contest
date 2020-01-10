import sys
from report_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import time

class father_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):                           #构造函数
        super(father_window, self).__init__()
        self.setupUi(self)
        self.pushButton.setIcon(QtGui.QIcon("./picture/plotsuolue2.png"))
        self.textBrowser.setText("ens33")
        localtime=time.asctime(time.localtime(time.time()))
        self.textBrowser_2.setText(str(localtime))
        with open('tongji2.txt',encoding='gbk',mode='r') as f:
            data = f.readlines()
            for a in data:
                self.listWidget.addItem(a)
        self.textBrowser_3.setText("192.168.56.130")
        self.textBrowser_4.setText("45.77.187.229")

    def show1(self):
        os.system("eog ./picture/plot2.png")
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = father_window()
    ex.show()
    sys.exit(app.exec_())
