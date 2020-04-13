from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt


class TrainModelWidget(QtWidgets.QWidget):
    """
    Custom Qt Widget for synbio_project GUI.
    Container for the buttons/functions of the "train model" button and subsequent menu options.
    """

    def __init__(self, *args, **kwargs):
        super(TrainModelWidget, self).__init__(*args, **kwargs)

        # train model main button
        train_model_btn = QtWidgets.QPushButton("Train Model")
        train_model_btn_menu = QtWidgets.QMenu()

        # add menu items
        random_data_action = QtWidgets.QAction("Use random data", self)
        random_data_action.triggered.connect(self.train_model) # connects menu item with function
        load_data_action = QtWidgets.QAction("Load data...", self)
        load_data_action.triggered.connect(self.load_data)

        train_model_btn_menu.addAction(random_data_action)
        train_model_btn_menu.addAction(load_data_action)

        train_model_btn.setMenu(train_model_btn_menu) # associates menu with button

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(train_model_btn)
        self.setLayout(layout)

    # placeholder function
    def train_model(self, input_data="random_data"):
        alert = QtWidgets.QMessageBox()
        alert.setText('Clicked use random data')
        alert.exec_()

    def load_data(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Select file to load data from.")

        # create widgets
        text_label = QtWidgets.QLabel("Supported file types: .csv, .txt, and .npy \
                                                              \nGo to [url for github docs] for example file formats.");

        # filepath input
        filepath_input = QtWidgets.QLineEdit("default filepath")

        # folder icon

        # button
        train_model_btn = QtWidgets.QPushButton("Train model with this data")
        # self.train_model_btn.clicked.connect(self.train_model("input_data"))

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(text_label)
        layout.addWidget(filepath_input)
        # add folder icon here
        layout.addWidget(train_model_btn)
        dialog.setLayout(layout)

        dialog.exec_()
