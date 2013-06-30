# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Sun Jun 30 23:51:08 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(425, 187)
        self.okButton = QtGui.QPushButton(AboutDialog)
        self.okButton.setGeometry(QtCore.QRect(320, 140, 91, 32))
        self.okButton.setObjectName("okButton")
        self.label = QtGui.QLabel(AboutDialog)
        self.label.setGeometry(QtCore.QRect(150, 10, 180, 19))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(AboutDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 101, 101))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/board-140px.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(AboutDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 148, 12))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(AboutDialog)
        self.label_4.setGeometry(QtCore.QRect(140, 90, 209, 12))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(AboutDialog)
        self.label_5.setGeometry(QtCore.QRect(200, 30, 61, 13))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(AboutDialog)
        self.label_6.setGeometry(QtCore.QRect(170, 60, 140, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtGui.QLabel(AboutDialog)
        self.label_7.setGeometry(QtCore.QRect(20, 160, 111, 12))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), AboutDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About Ultimate TTT", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("AboutDialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AboutDialog", "Ultimate Tic-Tac-Toe", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AboutDialog", "Copyright (C) 2013 Filipe Maia", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("AboutDialog", "<html><head/><body><p><a href=\"https://github.com/FilipeMaia/ultimate_ttt\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/FilipeMaia/ultimate_ttt</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("AboutDialog", "Version 1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("AboutDialog", "Created by Filipe Maia", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("AboutDialog", "<html><head/><body><p><a href=\"http://creativecommons.org/licenses/by/3.0/\"><span style=\" text-decoration: underline; color:#0000ff;\">Link to License</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import ultimate_ttt_rc
