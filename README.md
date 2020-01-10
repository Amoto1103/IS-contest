# 基于流量分析的挖矿木马检测系统 #
****

## 目录 ##
[系统简介](#系统简介)    
[使用说明](#使用说明)    
[相关资料](#相关资料)


## 系统简介 ##
----------------------

## 使用说明 ##
-----------------------

### 环境配置 ###

系统要求：Ubuntu 16.04 及以上（这里只按照16.04写）

为了运行界面，需要安装python3及一些库函数：

1.  安装python3.5 （大部分Ubuntu1604镜像自带）
2.  安装pip3：  *`sudo apt install python3-pip`*
3.  安装pyqt5：  *`sudo pip3 install pyqt5`*
4.  安装tkinter：  *`sudo apt install python3-tk`*
5.  安装numpy：  *`sudo apt install numpy`*

以上安装完成后可以运行起界面，为了运行检测的功能，还需要安装libpcap，以下给出简单的安装过程：

1.  libpcap关联的安装包已经下载好，放在packets文件中，如果需要最新版本可以在官网上重新下载，解压缩packets文件夹的4个压缩包；
2.  分别进入4个文件夹，依照顺序（m4、bison、flex、libpcap）用`cd`进入，分别运行：
     - *`sudo ./configure`*
     - *`sudo make`*
     - *`sudo make install`*

运行时会出现libpcap.so.1找不到的情况，需要手动改一下其环境变量：

1.  查找libpcap.so.1的位置，比如*/usr/local/lib*；
2.  以管理员编辑*/etc/ld.so.conf*，将位置添加在下面，执行*`sudo ldconfig`*

至此环境配置结束，可以正式开始检测了！

### 检测挖矿 ###

## 相关资料 ##