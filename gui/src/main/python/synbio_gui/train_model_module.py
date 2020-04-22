from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from file_dialog import FileDialog


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
        self.setFixedSize(500, 150)

        # train model main button
        train_model_btn = QtWidgets.QPushButton("Train Model")
        train_model_btn_menu = QtWidgets.QMenu()

        # add menu items
        random_data_action = QtWidgets.QAction("Use random data", self)
        random_data_action.triggered.connect(lambda:self.train_model(input_data="random_data")) # connects menu item with function
        load_data_action = QtWidgets.QAction("Load data...", self)
        load_data_action.triggered.connect(self.load_data)

        train_model_btn_menu.addAction(random_data_action)
        train_model_btn_menu.addAction(load_data_action)

        train_model_btn.setMenu(train_model_btn_menu) # associates menu with button

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(train_model_btn)
        self.setLayout(layout)

        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        cursor = self.console_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()

    # placeholder function
    def train_model(self, input_data=None):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Training model...")
        dialog.setFixedSize(600, 500)

        label = QtWidgets.QLabel("Training model using " + str(input_data))

        self.console_output = QtWidgets.QTextEdit()
        self.console_output.moveCursor(QtGui.QTextCursor.Start)
        self.console_output.ensureCursorVisible()
        self.console_output.setLineWrapColumnOrWidth(500)
        self.console_output.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)

        print('lalalala testing')
        print('testing line 2')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.console_output)

        dialog.setLayout(layout)
        dialog.exec_()

    def load_data(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Select file to load data from")

        # create widgets
        text_label = QtWidgets.QLabel("Supported file types: .csv, .txt, and .npy \
                                                              \nGo to [url for github docs] for example file formats.");

        # filepath widget
        filepath = FileDialog()

        # buttons
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.close)

        train_model_btn = QtWidgets.QPushButton("Train model with this data")
        train_model_btn.clicked.connect(lambda:self.train_model(input_data="input_data"))

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(train_model_btn)

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(text_label)
        layout.addWidget(filepath)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        dialog.exec_()
