from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from PyQt5.QtWidgets import (QLabel, QSlider, QPlainTextEdit, QRadioButton, QPushButton, QComboBox, QVBoxLayout, QStackedLayout,
                             QApplication, QWidget)
from PyQt5.QtCore import Qt
from file_dialog import FileDialog, MultiFileDialog
from utils import get_saved_models
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from backend.cross_talk_evaluator import CrossTalkEvaluator
from data_loader import DataLoaderWidget
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors as mcolors
from matplotlib.ticker import FuncFormatter

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
plt.style.use('seaborn-dark')

project_root = os.environ.get('PYTHONPATH')

project_root = os.environ.get('PYTHONPATH')
try:
    project_root = project_root.split(os.path.pathsep)[1]
except Exception as e:
    pass


class RMW(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(RMW, self).__init__(*args, **kwargs)

        rm_button = QtWidgets.QPushButton("Run Model")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(rm_button)
        self.setLayout(layout)

        self.path = project_root
        self.currentmodel = ""
        self.dna1 = ""
        self.dna2 = ""
        self.initial = 1
        self.canvas = ""
        self.ok = ""
        self.layout = ""

        if os.path.exists(os.path.join(self.path, 'models')):
            rm_button.clicked.connect(self.evalparam)
        else:
            rm_button.clicked.connect(self.nomodel)

        self.cross_talk_evaluator = CrossTalkEvaluator()
        self.bind1 = ""
        self.bind2 = ""
        self.threshold = 0.5
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.threshold_change)

    def nomodel(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Error")
        error = QtWidgets.QLabel("There are currently no models.")
        ok = QtWidgets.QPushButton("OK")
        ok.clicked.connect(dialog.close)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(error)
        dialog.setLayout(layout)
        dialog.exec_()

    def evalparam(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Evaluation Parameters")

        label1 = QtWidgets.QLabel("Choose Model")
        combo = QComboBox(self)
        combo.addItems(get_saved_models())

        self.currentmodel = str(combo.currentText())
        self.cross_talk_evaluator.load_model(self.currentmodel)

        label2 = QtWidgets.QLabel("Input sequences")

        label3 = QRadioButton("Manual entry")
        label3.setChecked(True)
        label4 = QRadioButton("Upload data file")
        label4.toggled.connect(self.uploaddata)

        label5 = QtWidgets.QLabel("(DNA sequence inputs can only be a max length of 300 b.p)")

        label6 = QtWidgets.QLabel("DNA Sequence 1")
        self.dna1 = QPlainTextEdit(self)
        self.dna1.textChanged.connect(self.dna_change)

        label7 = QtWidgets.QLabel("DNA Sequence 2")
        self.dna2 = QPlainTextEdit(self)
        self.dna2.textChanged.connect(self.dna_change)

        cancel = QtWidgets.QPushButton("Cancel")
        cancel.clicked.connect(dialog.close)
        self.ok = QtWidgets.QPushButton("OK")
        self.ok.clicked.connect(lambda: self.threshold_change())
        self.ok.setEnabled(False)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel)
        button_layout.addWidget(self.ok)

        buttonlayout = QtWidgets.QHBoxLayout()
        buttonlayout.addWidget(label3)
        buttonlayout.addWidget(label4)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(combo)
        layout.addWidget(label2)
        layout.addLayout(buttonlayout)
        layout.addWidget(label5)
        layout.addWidget(label6)
        layout.addWidget(self.dna1)
        layout.addWidget(label7)
        layout.addWidget(self.dna2)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        dialog.exec_()

    def dna_change(self):
        self.bind1, self.bind2 = self.cross_talk_evaluator.run(self.dna1.toPlainText().rstrip(),
                                                               self.dna2.toPlainText().rstrip())
        if (len(self.dna1.toPlainText().rstrip()) <= 300 or len(self.dna2.toPlainText().rstrip()) <= 300):
            self.ok.setEnabled(False)
        else:
            self.ok.setEnabled(True)

    def uploaddata(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Evaluation Parameters")
        up_data = self.sender()
        if up_data.isChecked():
            label = QtWidgets.QLabel("Supported file types: .csv, .txt, and .npy \
                                                                          \nGo to [url for github docs] for example file formats.")

            filepath = DataLoaderWidget()

            cancel = QtWidgets.QPushButton("Cancel")
            cancel.clicked.connect(dialog.close)
            self.ok = QtWidgets.QPushButton("OK")
            self.ok.clicked.connect(lambda: self.threshold_change())
            self.ok.setEnabled(False)

            button_layout = QtWidgets.QHBoxLayout()
            button_layout.addWidget(cancel)
            button_layout.addWidget(self.ok)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(filepath)
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec_()

    def initial_draw(self):
        size1 = len(self.bind1) * 300
        size2 = len(self.bind2) * 300

        size = size1 if size1 > size2 else size2

        size = 1.01 * size

        self.figure = plt.figure(figsize=(20, 10))
        ax1 = self.figure.add_subplot(2, 1, 1)
        self.line1 = self.plot_seq_bindings(ax1, size, self.bind1, 'DNA seq 1', "DNA base position", "Binding values",
                                            self.threshold)

        ax2 = self.figure.add_subplot(2, 1, 2)
        self.line2 = self.plot_seq_bindings(ax2, size, self.bind2, 'DNA seq 2', "DNA base position", "Binding values",
                                            self.threshold)

        self.figure.suptitle("Cross Talk for Transcription Factor: " + str(self.currentmodel), fontsize=25)
        self.canvas = FigureCanvas(self.figure)
        self.initial = 0
        self.dialog = QtWidgets.QDialog(self)
        self.dialog.setWindowTitle("Output graph")

    def threshold_change(self):
        self.threshold = self.slider.value() / 100

        if self.initial:
            self.initial_draw()
        else:
            self.update_plot()

        self.canvas.draw()

        layout = QVBoxLayout()
        label = QLabel("Threshold")
        layout.addWidget(label)
        layout.addWidget(self.slider)
        layout.addWidget(self.canvas)
        self.dialog.setLayout(layout)
        self.dialog.exec_()

    def plot_seq_bindings(self, ax, xlim, bindings, legend, xlabel, ylabel, threshold):
        size = [i * self.cross_talk_evaluator.model.input_length for i in range(len(bindings))]
        ax.plot(size, bindings, label=legend)
        line, = ax.plot(size, [threshold for _ in range(len(bindings))], label='threshold', color=colors['darkred'])
        ax.legend(fontsize=15)
        ax.grid()
        ax.set_ylim(0, 1.01)
        ax.set_xlim(0, xlim)
        ax.set_xticklabels(ax.get_xticks(), {'size': 13})
        ax.set_yticklabels(ax.get_yticks(), {'size': 13})
        ax.xaxis.set_major_formatter(FuncFormatter(self.integers))
        ax.yaxis.set_major_formatter(FuncFormatter(self.one_decimal))
        ax.set_ylabel(ylabel, fontsize=15)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=15)

        return line

    def update_plot(self):
        self.line1.set_ydata([self.threshold for _ in range(len(self.bind1))])
        self.line2.set_ydata([self.threshold for _ in range(len(self.bind2))])

    def integers(self, x, pos):
        return '%1d' % x

    def one_decimal(self, y, pos):
        return '%1.1f' % y
