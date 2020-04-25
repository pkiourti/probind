from PyQt5 import QtCore, QtGui, QtWidgets
from file_dialog import FileDialog, MultiFileDialog

import utils


class ManageModelWidget(QtWidgets.QWidget):
    """
    Custom Qt Widget for synbio_project GUI.
    Container for the buttons/functions of the "manage models" button and subsequent menu options.
    """

    def __init__(self, *args, **kwargs):
        super(ManageModelWidget, self).__init__(*args, **kwargs)
        self.setFixedWidth(250)

        # train model main button
        manage_model_btn = QtWidgets.QPushButton("Manage Models")
        manage_model_btn_menu = QtWidgets.QMenu()

        # add menu items
        delete_action = QtWidgets.QAction("Delete Model", self)
        delete_action.triggered.connect(lambda:self.input_dialog(True))
        rename_action = QtWidgets.QAction("Rename model", self)
        rename_action.triggered.connect(lambda:self.input_dialog())

        manage_model_btn_menu.addAction(delete_action)
        manage_model_btn_menu.addAction(rename_action)
        manage_model_btn.setMenu(manage_model_btn_menu) # associates menu with button

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(manage_model_btn)
        self.setLayout(layout)

    def input_dialog(self, delete=False):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select file to modify")

        file_label = QtWidgets.QLabel("File: ")
        filepath = FileDialog() # select which file to change
        filepath.filter = ""
        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(file_label)
        file_layout.addWidget(filepath)

        newname_frame = QtWidgets.QFrame()

        new_name_label = QtWidgets.QLabel("New name: ")
        new_name_input = QtWidgets.QLineEdit()
        new_name_input.setPlaceholderText("[new name]")
        new_name_layout = QtWidgets.QHBoxLayout()
        new_name_layout.addWidget(new_name_label)
        new_name_layout.addWidget(new_name_input)
        newname_frame.setLayout(new_name_layout)

        if delete:
            newname_frame.hide()

        # buttons
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.close)

        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.clicked.connect(dialog.close)

        ok_btn.clicked.connect(lambda: self.check_inputs(inputs=[filepath.filepath, new_name_input.text()], delete=delete))

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(file_layout)
        # layout.addLayout(new_name_layout)
        layout.addWidget(newname_frame)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        dialog.exec_()

    def check_inputs(self, inputs, delete):
        invalid_inputs = False

        if len(inputs) == 0:
            invalid_inputs = True
        else:
            if delete:
                if inputs[0] == "":
                    invalid_inputs = True
            else:
                for i in inputs:
                    if i == "":
                        invalid_inputs = True
                        break  # error message only appears once

        if invalid_inputs:
                alert = QtWidgets.QMessageBox()
                alert.setText("Input must be non-empty")
                alert.setWindowTitle("Invalid input")
                alert.setIcon(QtWidgets.QMessageBox.Warning)
                alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
                alert.exec_()
        else:
            if delete:
                try:
                    utils.delete_model(inputs[0])
                    alert = QtWidgets.QMessageBox()
                    alert.setText("File deleted")
                    alert.setWindowTitle("Confirmation")
                    alert.setIcon(QtWidgets.QMessageBox.Information)
                    alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    alert.exec_()
                except:
                    print("File not deleted.")
            # else: # rename