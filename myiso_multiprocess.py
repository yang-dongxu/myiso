# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\yangdongxu\OneDrive - hk sar baomin inc\桌面\myiso\myiso_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog,QDialog,QMessageBox
from read_data import readdata
import os
import _thread
import threading
from multiprocessing import Pool,Process 




class myThread(threading.Thread):
    counter=0

    @classmethod
    def add_count(cls):
        cls.counter+=1
    
    @classmethod
    def reduce_count(cls):
        cls.counter-=1

    def __init__(self, file_name):
        super().__init__()
        self.file_name=file_name
        self.add_count()

    def run(self):
        print ('start %s'%self.file_name)
        readdata(self.file_name)
        print ('end %s'%self.file_name)
        self.reduce_count()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(437, 300)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton.setGeometry(QtCore.QRect(50, 40, 191, 19))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton_2.setGeometry(QtCore.QRect(50, 70, 361, 19))
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 190, 93, 28))
        self.pushButton.setCheckable(False)
        self.pushButton.setChecked(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(100, 140, 231, 16))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.file_or_path)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "mysio"))
        self.radioButton.setText(_translate("MainWindow", "选择单个文件"))
        self.radioButton_2.setText(_translate("MainWindow", "选择文件夹，内仅包含多个同一格式的数据文件"))
        self.pushButton.setText(_translate("MainWindow", "Choose"))
        self.label.setText(_translate("MainWindow", "file_path"))

    def file_or_path(self):
        
        if self.radioButton.isChecked():
            po=Pool()
            filename,i=QFileDialog.getOpenFileName(None,'choose the file')
            self.label.setText(filename.split('/')[-1])
            po.apply_async(readdata,(filename,))
            #readdata(filename)
            po.close()
        else:
            po=Pool()
            pathname=QFileDialog.getExistingDirectory(None,'choose the directory')
            filenames=os.listdir(pathname)
            for i in filenames:
                po.apply_async(readdata,(pathname+'/'+i,))
                #myThread(pathname+'/'+i).start()
                #readdata(pathname+'/'+i)
                self.label.setText(i)
            po.close()
        po.join()
        QMessageBox.information(None,'note','the file is processed', QMessageBox.Yes)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
