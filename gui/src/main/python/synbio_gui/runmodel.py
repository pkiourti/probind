from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import (QLabel, QRadioButton, QPushButton, QComboBox, QVBoxLayout, QApplication, QWidget, QLineEdit, QMessageBox)
from file_dialog import FileDialog

class RMW(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(RMW, self).__init__(*args, **kwargs)

        rm_button = QtWidgets.QPushButton("Run Model")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(rm_button)
        self.setLayout(layout)
        rm_button.clicked.connect(self.evalparam)

    def run_model(self): # will fix later; this is the graph stuff
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Output graph")

        dialog.setLayout(layout)
        dialog.exec_()


    def evalparam(self): # have to fix layout -- meaning sizes/placements of widgets etc
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Evaluation Parameters")

        label1 = QtWidgets.QLabel("Choose Model")
        combo = QComboBox(self)
        # need to add list of stuff to put in combo box
        # make sure it's list of user inputs

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
        ok = QtWidgets.QPushButton("OK") # not working rn -- will fix this and clicked.connect
        #ok.clicked.connect()

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

    def uploaddata(self): # stuff is commented out rn bc i'm trying to get rid of the dialog thing
       # dialog = QtWidgets.QDialog(self)
      #  dialog.setWindowTitle("Evaluation Parameters")
        up_data = self.sender()
        if up_data.isChecked():
            label = QtWidgets.QLabel("Supported file types: .csv, .txt, and .npy \
                                                                          \nGo to [url for github docs] for example file formats.");

            filepath = FileDialog()  # using Thuy's code

            #cancel = QtWidgets.QPushButton("Cancel")
            #cancel.clicked.connect(dialog.close)
            #ok = QtWidgets.QPushButton("OK")
            #ok.clicked.connect(lambda: self.run_model(input_data="input_data"))

            # button_layout = QtWidgets.QHBoxLayout()
            # button_layout.addWidget(cancel)
            # button_layout.addWidget(ok)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(filepath)
            # layout.addLayout(button_layout)
            # dialog.setLayout(layout)
            # dialog.exec_()