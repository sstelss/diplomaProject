from PyQt5 import QtWidgets, QtCore
import sys
import data_formats as df
import simulated_annealing as sim
import ant_thread as ant
import gibrid_al as gb
import new_bee as nb
import os

from ui_form_index import *

class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    # метод позволяющий принять значения для потока
    def prepare(self, info_stat_t, path):
        self.info_stat = info_stat_t
        self.path = path
        self.start()
    # непосредственно запуск потока
    def run(self):

        with open("result.txt", "w") as f:
            print("Result: ", file=f)
        if self.info_stat[0]:
            result_ant = ant.run(self.path, alpha=0.7, beta=1.3, count=38, t_live=100, e=10, p=0.7, Q=1)
            with open("result.txt", "a") as f:
                print("Ant colony algorithm   ", result_ant, file=f)
        if self.info_stat[1]:
            pass
            # with open("result.txt", "a") as f:
            #     print("Bee result                  ", result_bee, file=f)
        if self.info_stat[2]:
            result_gib = gb.run(self.path, alpha=0.7, beta=1.3, gamma=0.3, count=38, t_live=100, p=0.7, Q=1)
            with open("result.txt", "a") as f:
                print("Gibrid    ", result_gib, file=f)
        if self.info_stat[3]:
            result_simul = sim.run(self.path, paint=0)
            with open("result.txt", "a") as f:
                print("Simulated                   ", result_simul, file=f)
        if self.info_stat[4]:
            result_bee = nb.run(self.path, n=100, amount=1000)
            with open("result.txt", "a") as f:
                print("Bee result                  ", result_bee, file=f)
        osCommandString = "notepad.exe result.txt"
        os.system(osCommandString)



class MyWindow1(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.path = 0
        QtWidgets.QWidget.__init__(self, parent)
        # экземпляр класса потока
        self.mythread = MyThread()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start)
        self.ui.pushButton_for_open_fille.clicked.connect(self.choose_path)
        # отслеживает запуск потока
        # self.mythread.started.connect(self.on_started)
        # отслеживает завершение потока
        self.mythread.finished.connect(self.on_finished)

    def start(self):

        if self.path == 0:
            QtWidgets.QMessageBox.about(self, "Уведомление", "Выбирете файл с вершинами!")
        else:
            # список состояний чекбоксов по порядку
            info_stat = [self.ui.checkBox_ant_colony.checkState(), self.ui.checkBox_genetic.checkState(),
                         self.ui.checkBox_gibrid.checkState(), self.ui.checkBox_imitation.checkState(),
                         self.ui.checkBox_bee.checkState()]

            if not any(info_stat):
                QtWidgets.QMessageBox.about(self, "Уведомление", "Выберите хотя бы один алгоритм!")
            else:
                # делаем кнопку неактивной
                self.ui.pushButton.setDisabled(True)
                self.ui.label_for_process.setText("Подождите! Идет вычисление.")
                # запускаем поток
                self.mythread.prepare(info_stat, self.path)


    def choose_path(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '')[0]
        self.ui.label_path_to_file.setText(str( fname))
        self.path = fname
        print(fname)

    def on_finished(self):
        self.ui.pushButton.setDisabled(False)
        self.ui.label_for_process.setText("Вычисление завершено!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow1()
    window.show()
    sys.exit(app.exec_())