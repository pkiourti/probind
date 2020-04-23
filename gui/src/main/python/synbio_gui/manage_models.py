from PyQt5 import QtCore, QtGui, QtWidgets
from file_dialog import FileDialog, MultiFileDialog


class ManageModelWidget(QtWidgets.QWidget):
    """
    Custom Qt Widget for synbio_project GUI.
    Container for the buttons/functions of the "manage models" button and subsequent menu options.
    """

    def __init__(self, *args, **kwargs):
        super(ManageModelWidget, self).__init__(*args, **kwargs)
        self.setFixedWidth(500)

        # train model main button
        manage_model_btn = QtWidgets.QPushButton("Manage Models")
        manage_model_btn_menu = QtWidgets.QMenu()

        # add menu items
        delete_action = QtWidgets.QAction("Delete Model", self)
        delete_action.triggered.connect(lambda:self.input_dialog())
        rename_action = QtWidgets.QAction("Rename model", self)
        rename_action.triggered.connect(lambda:self.input_dialog(True))

        manage_model_btn_menu.addAction(delete_action)
        manage_model_btn_menu.addAction(rename_action)
        manage_model_btn.setMenu(manage_model_btn_menu) # associates menu with button

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(manage_model_btn)
        self.setLayout(layout)

    def input_dialog(self, delete=False):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select file to modify")

        filepath = FileDialog() # select which file to change

        new_name_label = QtWidgets.QLabel("New name: ")
        new_name_input = QtWidgets.QLineEdit()
        new_name_input.setPlaceholderText("[new name]")
        new_name_layout = QtWidgets.QHBoxLayout()
        new_name_layout.addWidget(new_name_label)
        new_name_layout.addWidget(new_name_input)
        new_name_layout.setVisible(False)

        # buttons
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.close)

        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.clicked.connect(dialog.close)

        if delete == True:
            new_name_layout.setVisible(True)
        #     # ok_btn.clicked.connect()
        # else:
        #     ok_btn.clicked.connect()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(filepath)
        layout.addLayout(new_name_layout)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)