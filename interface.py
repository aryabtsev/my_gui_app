import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QLabel, QRadioButton, QSpinBox, QDial)
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QCoreApplication

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.ptime import time

import numpy as np

from ECG_Generator import ECGen

import random

class AlgoGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()



    def initUI(self):

        # Подсказка
        QToolTip.setFont (QFont('Times', 12))
        self.setToolTip('Это программа реализующая тестирование алгоритма адаптирования частоты кардиостимуляции')
        self.setToolTipDuration(1500)


        # Надписи
        lbl1 = QLabel('Сигнал ЭКГ', self)
        #lbl1.move(210, 10)

        lbl2 = QLabel('Сигнал кардиостимулятора', self)
        #lbl2.move(170, 220)

        #виджеты графиков pygraph
        ecg_plot = pg.PlotWidget()
        curve = ecg_plot.plot(pen='g')
        fps = None

        cs_plot = pg.PlotWidget()
        curve_cs = cs_plot.plot(pen='r')

        def get_ecg(value):
            data = ECGen.ecg_gen_norm(value)
            return data


        def start_callback():
            if radio1:
                # 1) Simplest approach -- update data in the array such that plot appears to scroll
                #    In these examples, the array size is fixed.

                data1 = get_ecg(spinner.value())

                curve1 = ecg_plot.plot(data1, pen = 'g')
                curve2 = cs_plot.plot(data1, pen = 'r')
                ptr1 = 0

                def update1():
                    global data1, curve1, ptr1
                    data1[:-1] = data1[1:]  # shift data in the array one sample left
                    # (see also: np.roll)
                    data1[-1] = (get_ecg(spinner.value())[0])
                    #curve1.setData(data1)

                    ptr1 += 1
                    curve2.setData(data1)
                    curve2.setPos(ptr1, 0)

        # Кнопка запуска
        btn = QPushButton('Старт', self)
        btn.setToolTip('Кнопка старта генерации ЭКГ сигнала')
        btn.setToolTipDuration(1500)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(start_callback)
        #btn.move(440, 400)

        # Кнопка закрытия
        closebtn = QPushButton('Закрыть', self)
        closebtn.setToolTip('Закрыть программу')
        closebtn.setToolTipDuration(1500)
        closebtn.clicked.connect(QCoreApplication.instance().quit)
        closebtn.resize(btn.sizeHint())
        #closebtn.move(440, 350)

        # Кнопки выбора режима генерации
        radio1 = QRadioButton('ЭКГ в норме', self)
        #radio1.move(440, 30)
        radio2 = QRadioButton('1 симптом', self)
        #radio2.move(440, 50)
        radio3 = QRadioButton('2 симптом', self)
        #radio3.move(440, 70)


        def value_change():
            dial.setValue(spinner.value())
        # Окно ввода частоты
        spinner = QSpinBox(self)
        spinner.setValue(72)
        spinner.setRange(20, 150)
        spinner.setGeometry(460, 120, 60, 20)
        spinner.valueChanged.connect(value_change)


        def value_changer():
            spinner.setValue(dial.value())

        # Ползунок вращатель
        dial = QDial(self)
        dial.setMinimum(20)
        dial.setMaximum(150)
        #dial.move(440, 150)
        dial.valueChanged.connect(value_changer)

        #layouts

        v_box1 = QtWidgets.QVBoxLayout()
        v_box1.addStretch()
        v_box1.addWidget(lbl1)
        v_box1.addWidget(ecg_plot)
        v_box1.addWidget(lbl2)
        v_box1.addWidget(cs_plot)
        v_box1.addStretch()

        v_box2 = QtWidgets.QVBoxLayout()
        v_box2.addSpacing(30)
        v_box2.addWidget(radio1)
        v_box2.addWidget(radio2)
        v_box2.addWidget(radio3)
        v_box2.addWidget(spinner)
        v_box2.addWidget(dial)
        v_box2.addWidget(btn)
        v_box2.addWidget(closebtn)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box1)
        h_box.addLayout(v_box2)
        h_box.addStretch()

        self.setLayout(h_box)

        #Cоздание окна
        self.setGeometry(300, 100, 750, 350)
        self.setWindowTitle('Алгоритм автоподстройки частоты')
        self.setWindowIcon(QIcon('/Desktop/028-512.png'))
        appearance = self.palette()
        appearance.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                            QtGui.QColor("light blue"))
        self.setPalette(appearance)

        self.main_widget = QWidget(self)

        self.show()

    # функция переопределяющая закрытие
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Вы точно хотите закрыть?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()






if __name__ == '__main__':


    app = QApplication(sys.argv)
    ex = AlgoGUI()
    sys.exit(app.exec_())