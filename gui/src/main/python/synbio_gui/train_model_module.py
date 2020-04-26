from backend.train_wrapper import TrainWrapper
import utils

from PyQt5 import QtCore, QtGui, QtWidgets
from data_loader import DataLoaderWidget
import sys
from file_dialog import FileDialog, MultiFileDialog
import os
import time
import shutil
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from worker import Worker


sig_abort_workers = QtCore.pyqtSignal()


class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class TrainModelWidget(QtWidgets.QWidget):
    """
    Custom Qt Widget for synbio_project GUI.
    Container for the buttons/functions of the "train model" button and subsequent menu options.
    """

    def __init__(self, *args, **kwargs):
        super(TrainModelWidget, self).__init__(*args, **kwargs)
        # self.setFixedWidth(250)

        # initialize variables to be referenced later throughout module
        self.model_name = ""
        self.num_epochs = 0
        self.input_params = None
        self.console_output = None
        self.x_fwd, self.x_rev, self.y = (None, None, None)
        self.train_wrapper = None

        # train model main button
        train_model_btn = QtWidgets.QPushButton("Train Model")
        train_model_btn_menu = QtWidgets.QMenu()

        # add menu items
        random_data_action = QtWidgets.QAction("Use random data", self)
        random_data_action.triggered.connect(lambda:self.input_train_params(True)) # connects menu item with function
        load_data_action = QtWidgets.QAction("Load data...", self)
        load_data_action.triggered.connect(lambda:self.input_train_params(False))

        train_model_btn_menu.addAction(random_data_action)
        train_model_btn_menu.addAction(load_data_action)

        train_model_btn.setMenu(train_model_btn_menu) # associates menu with button

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(train_model_btn)
        self.setLayout(layout)

        sys.stdout = Stream(newText=self.on_update_text)

    def input_train_params(self, use_random_data=True):
        self.input_params = QtWidgets.QDialog(self)
        self.input_params.setWindowTitle("Set training parameters...")
        self.input_params.setFixedSize(450, 200)

        explanation_text = QtWidgets.QLabel("Please enter model parameters below.\
                                            Choose a name to save the model as (max 255 chars, alphanumeric only)\
                                            and the number of epochs to train the model for (int only).")
        explanation_text.setWordWrap(True)

        name_label = QtWidgets.QLabel("Model name")
        name_input = QtWidgets.QLineEdit()
        name_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9_]{0,255}"))) # only up to 255 alphanumeric chars
        name_group = QtWidgets.QHBoxLayout()
        name_group.addWidget(name_label)
        name_group.addWidget(name_input)

        epoch_label = QtWidgets.QLabel("# training epochs")
        epoch_input = QtWidgets.QLineEdit()
        epoch_input.setValidator(QtGui.QIntValidator()) # int only
        epoch_group = QtWidgets.QHBoxLayout()
        epoch_group.addWidget(epoch_label)
        epoch_group.addWidget(epoch_input)

        # buttons
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.input_params.close)

        ok_btn = QtWidgets.QPushButton("OK")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(explanation_text)
        layout.addLayout(name_group)
        layout.addLayout(epoch_group)
        layout.addLayout((button_layout))

        self.input_params.setLayout(layout)

        if not use_random_data:
            ok_btn.clicked.connect(lambda:self.check_nonempty_inputs([name_input.text(), epoch_input.text()], False))
        else:
            ok_btn.clicked.connect(lambda: self.check_nonempty_inputs([name_input.text(), epoch_input.text()]))

        self.input_params.exec_()

    # checks for non-empty model parameter inputs
    def check_nonempty_inputs(self, inputs=[], use_random_data=True):
        invalid_inputs = False

        if len(inputs) == 0:
            invalid_inputs = True
        else:
            for i in inputs:
                if i == "":
                    invalid_inputs = True
                    break # error message only appears once

        if invalid_inputs:
            alert = QtWidgets.QMessageBox()
            alert.setText("Input must be non-empty")
            alert.setWindowTitle("Invalid input")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
            alert.exec_()
        else: # inputs are valid
            self.input_params.close()
            new_name = inputs[0]
            self.num_epochs = int(inputs[1])

            name_exists = utils.check_avail_model_name(inputs[0])

            i = 1
            while(name_exists == True):
                new_name = inputs[0] + "_" + str(i)
                name_exists = utils.check_avail_model_name(new_name)
                i += 1

            self.model_name = new_name

            if use_random_data:
                self.train_model_dialog()
            else:
                # self.load_data()
                load_data_dialog = DataLoaderWidget()
                self.x_fwd = load_data_dialog.x_fwd
                self.x_rev = load_data_dialog.x_rev
                self.y = load_data_dialog.y
                self.train_model_dialog(random_data=False)

    def on_update_text(self, text):
        cursor = self.console_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()

    def train_model_dialog(self, random_data=True):
        if random_data:
            self.x_fwd, self.x_rev, self.y = utils.choose_random_input_data()
            input_str = "random data"
        else:
            input_str = "selected input data"

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Training model...")
        dialog.setFixedSize(600, 500)

        label = QtWidgets.QLabel("Training model using " + input_str)

        self.console_output = QtWidgets.QTextEdit()
        self.console_output.moveCursor(QtGui.QTextCursor.Start)
        self.console_output.ensureCursorVisible()
        self.console_output.setLineWrapColumnOrWidth(500)
        self.console_output.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)

        self.train_wrapper = TrainWrapper(self.num_epochs, self.x_fwd, self.x_rev, self.y, self.model_name)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.console_output)

        worker = Worker(self.train_wrapper)
        thread = QtCore.QThread()
        worker.moveToThread(thread)

        # get progress messages from worker:
        worker.sig_done.connect(lambda:self.plot_loss_figure(worker.train_wrapper.get_figure()))
        # worker.sig_done.connect(thread.quit())
        worker.sig_msg.connect(lambda:self.update_output_log(worker.text))

        thread.started.connect(worker.work)
        thread.start()

        dialog.setLayout(layout)
        dialog.exec_()

    def update_output_log(self, new_text):
        self.console_output.setText(new_text)

    def plot_loss_figure(self, figure):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Training Loss Plot")

        canvas = FigureCanvas(figure)

        # refresh canvas
        canvas.draw()

        ok_btn = QtWidgets.QPushButton("Ok")
        ok_btn.clicked.connect(dialog.close)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)
        layout.addWidget(ok_btn)

        dialog.setLayout(layout)
        dialog.exec_()