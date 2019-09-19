# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Олег/PycharmProjects/Makarov/index.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(432, 357)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_for_open_file = QtWidgets.QLabel(self.centralwidget)
        self.label_for_open_file.setObjectName("label_for_open_file")
        self.verticalLayout.addWidget(self.label_for_open_file)
        self.pushButton_for_open_fille = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_for_open_fille.setDefault(False)
        self.pushButton_for_open_fille.setFlat(False)
        self.pushButton_for_open_fille.setObjectName("pushButton_for_open_fille")
        self.verticalLayout.addWidget(self.pushButton_for_open_fille)
        self.label_path_to_file = QtWidgets.QLabel(self.centralwidget)
        self.label_path_to_file.setText("")
        self.label_path_to_file.setObjectName("label_path_to_file")
        self.verticalLayout.addWidget(self.label_path_to_file)
        self.label_for_choose = QtWidgets.QLabel(self.centralwidget)
        self.label_for_choose.setObjectName("label_for_choose")
        self.verticalLayout.addWidget(self.label_for_choose)
        self.checkBox_ant_colony = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_ant_colony.setCheckable(True)
        self.checkBox_ant_colony.setChecked(False)
        self.checkBox_ant_colony.setTristate(False)
        self.checkBox_ant_colony.setObjectName("checkBox_ant_colony")
        self.verticalLayout.addWidget(self.checkBox_ant_colony)
        self.checkBox_genetic = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_genetic.setObjectName("checkBox_genetic")
        self.verticalLayout.addWidget(self.checkBox_genetic)
        self.checkBox_gibrid = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_gibrid.setObjectName("checkBox_gibrid")
        self.verticalLayout.addWidget(self.checkBox_gibrid)
        self.checkBox_imitation = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_imitation.setObjectName("checkBox_imitation")
        self.verticalLayout.addWidget(self.checkBox_imitation)
        self.checkBox_bee = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_bee.setObjectName("checkBox_bee")
        self.verticalLayout.addWidget(self.checkBox_bee)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.label_for_process = QtWidgets.QLabel(self.centralwidget)
        self.label_for_process.setText("")
        self.label_for_process.setObjectName("label_for_process")
        self.verticalLayout.addWidget(self.label_for_process)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 432, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_for_open_file.setText(_translate("MainWindow", "Выбирите файл:"))
        self.pushButton_for_open_fille.setText(_translate("MainWindow", "Открыть"))
        self.label_for_choose.setText(_translate("MainWindow", "Выбирите методы которыми необходимо решить задачу:"))
        self.checkBox_ant_colony.setToolTip(_translate("MainWindow", "<html><head/><body><p>Метод муравьиной колонии в классической реализации</p></body></html>"))
        self.checkBox_ant_colony.setText(_translate("MainWindow", "Муравьиной колонии"))
        self.checkBox_genetic.setToolTip(_translate("MainWindow", "<html><head/><body><p>Класический генетический алгоритм</p></body></html>"))
        self.checkBox_genetic.setText(_translate("MainWindow", "Генетический"))
        self.checkBox_gibrid.setToolTip(_translate("MainWindow", "<html><head/><body><p>Гибрид алгоритма муравьиной колонии и генетического алгоритма</p></body></html>"))
        self.checkBox_gibrid.setText(_translate("MainWindow", "Гибридный"))
        self.checkBox_imitation.setText(_translate("MainWindow", "Иммитации отжига"))
        self.checkBox_bee.setText(_translate("MainWindow", "Пчелиной колонии"))
        self.pushButton.setText(_translate("MainWindow", "Старт"))

