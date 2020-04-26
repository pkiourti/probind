from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import (QLabel, QRadioButton, QPushButton, QComboBox, QVBoxLayout, QApplication, QWidget, QLineEdit, QMessageBox)
#from cross_talk_evaluator import CrossTalkEvaluator
from utils import get_saved_models
import os
from file_dialog import FileDialog

class RMW(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(RMW, self).__init__(*args, **kwargs)

        rm_button = QtWidgets.QPushButton("Run Model")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(rm_button)
        self.setLayout(layout)
        rm_button.clicked.connect(self.evalparam)

    def run_model(self): # output graph
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Output graph")



        dialog.exec_()

    def evalparam(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Evaluation Parameters")

        label1 = QtWidgets.QLabel("Choose Model")
        combo = QComboBox(self)
        # items in combo box will be from train model/manage model

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
        ok = QtWidgets.QPushButton("OK") #ok --> disable if no model
        ok.clicked.connect(lambda: self.run_model()) # error check for valid inputs?

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

            filepath = FileDialog()

            cancel = QtWidgets.QPushButton("Cancel")
            cancel.clicked.connect(dialog.close)
            ok = QtWidgets.QPushButton("OK")
            ok.clicked.connect(lambda: self.run_model()) # error check for valid inputs? -- disable if no model

            button_layout = QtWidgets.QHBoxLayout()
            button_layout.addWidget(cancel)
            button_layout.addWidget(ok)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(filepath)
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec_()