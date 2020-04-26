from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from PyQt5.QtWidgets import (QLabel, QSlider, QRadioButton, QPushButton, QComboBox, QVBoxLayout, QApplication, QWidget, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from file_dialog import FileDialog, MultiFileDialog
from utils import get_saved_models
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from backend.cross_talk_evaluator import CrossTalkEvaluator

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

        if os.path.exists(os.path.join(self.path, 'models')):
            rm_button.clicked.connect(self.evalparam)
        else:
            rm_button.clicked.connect(self.nomodel)

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


    def run_model(self): # output graph
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Output graph")

        slider = QSlider(Qt.Vertical)
        slider.setMinimum(0)
        slider.setMaximum(1)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setSingleStep(1)
        slider.setTickInterval(0.1)
     #   slider.valueChanged[int].connect(self.threshold)

        cross_talk_eval = CrossTalkEvaluator('name of the model')

        # seq1, seq2 can be either strings or numpy arrays (I accept both and have tested it)
        bind_values_1, bind_values_2 = cross_talk_eval.run(seq1,seq2)
        figure = plot_bindings(threshold, bind_values_1, bind_values_2)

        canvas = FigureCanvas(figure)
        canvas.draw()

        layout = QVBoxLayout()
        label = QLabel("Threshold")
        layout.addWidget(label)
        layout.addWidget(slider)
        dialog.setLayout(layout)
        dialog.exec_()

    #def threshold(self,value): # for graphs

    def evalparam(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Evaluation Parameters")

        label1 = QtWidgets.QLabel("Choose Model")
        combo = QComboBox(self)
        combo.addItems(get_saved_models())

        label2 = QtWidgets.QLabel("Input sequences")

        label3 = QRadioButton("Manual entry")
        label3.setChecked(True)
        label4 = QRadioButton("Upload data file")
        label4.toggled.connect(self.uploaddata)

        label5 = QtWidgets.QLabel("(DNA sequence inputs can only be a max length of 300 b.p)")

        label6 = QtWidgets.QLabel("DNA Sequence 1")
        textbox1 = QLineEdit(self)

        label7 = QtWidgets.QLabel("DNA Sequence 2")
        textbox2 = QLineEdit(self)

        cancel = QtWidgets.QPushButton("Cancel")
        cancel.clicked.connect(dialog.close)
        ok = QtWidgets.QPushButton("OK")
        ok.clicked.connect(lambda: self.run_model()) # error check for valid inputs -- textbox has nothing then display error

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel)
        button_layout.addWidget(ok)

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
        layout.addWidget(textbox1)
        layout.addWidget(label7)
        layout.addWidget(textbox2)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        dialog.exec_()

    def uploaddata(self):
       dialog = QtWidgets.QDialog(self)
       dialog.setWindowTitle("Evaluation Parameters")
       up_data = self.sender()
       if up_data.isChecked():
            label = QtWidgets.QLabel("Supported file types: .csv, .txt, and .npy \
                                                                          \nGo to [url for github docs] for example file formats.");

            filepath_dialog = FileDialog()
            filepath_dialog.directory = os.path.join(filepath_dialog.directory, 'data')
            filepath_dialog.filter = "Text, CSV files (*.txt; *.csv);; Text files (*.txt);; CSV files (*.csv)"
            npy_filepaths_dialog = MultiFileDialog()
            npy_filepaths_dialog.directory = os.path.join(npy_filepaths_dialog.directory, 'data')
            npy_filepaths_dialog.filter = "Numpy files (*.npy)"
            npy_filepaths_dialog.setVisible(False)

            csv_txt_btn.toggled.connect(lambda: filepath_dialog.setVisible(True))
            csv_txt_btn.toggled.connect(lambda: npy_filepaths_dialog.setVisible(False))
            npy_btn.toggled.connect(lambda: filepath_dialog.setVisible(False))
            npy_btn.toggled.connect(lambda: npy_filepaths_dialog.setVisible(True))

            cancel = QtWidgets.QPushButton("Cancel")
            cancel.clicked.connect(dialog.close)
            ok = QtWidgets.QPushButton("OK")
            ok.clicked.connect(lambda: self.run_model())

            button_layout = QtWidgets.QHBoxLayout()
            button_layout.addWidget(cancel)
            button_layout.addWidget(ok)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(filepath_dialog)
            layout.addWidget(npy_filepaths_dialog)
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec_()