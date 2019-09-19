import sys

from PyQt5 import QtWidgets

class Tabs(QtWidgets.QTabWidget):

    def __init__(self):
        super(Tabs, self).__init__()
        self.all_tabs = [QtWidgets.QWidget(), QtWidgets.QWidget()]
        # self.setTabsClosable(True)
        self.build_widgets()

    def build_widgets(self):
        self.addTab(self.all_tabs[0], 'Расчеты')
        self.addTab(self.all_tabs[1], 'Результаты')

        self.all_tabs[0].setLayout(QtWidgets.QVBoxLayout())
        self.all_tabs[0].layout().addWidget(QtWidgets.QPushButton('Новая вкладка'))

        self.all_tabs[1].setLayout(QtWidgets.QVBoxLayout())
        self.all_tabs[1].layout().addWidget(QtWidgets.QLabel("aeeeeeeeeeeee!"))

        # Достаем первый виджет из layout и задаем ему сигнал
        self.all_tabs[0].layout().itemAt(0).widget().clicked.connect(self.create_tab)

    def create_tab(self):
        self.all_tabs.append(QtWidgets.QWidget())
        self.addTab(self.all_tabs[len(self.all_tabs) - 1],
                    'Tab {}'.format(len(self.all_tabs)))



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabs_area = Tabs()
        self.setCentralWidget(self.tabs_area)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec_())