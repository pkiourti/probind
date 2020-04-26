from PyQt5 import QtCore, QtGui, QtWidgets

import os

project_root = os.environ.get('PYTHONPATH')
try:
    project_root = project_root.split(os.path.pathsep)[1]
except Exception as e:
    pass


class FileDialog(QtWidgets.QWidget):
    """
    Module for Qt Widget for 'Open File Dialog'
    """

    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setFixedWidth(750)

        # filepath input
        self.filepath_input = QtWidgets.QLineEdit()
        self.filepath_input.setPlaceholderText("default filepath")
        self.filepath = ""
        self.directory = project_root
        self.filter = "Text, CSV, or Numpy files (*.txt; *.csv; *.npy);; \
                    Text files (*.txt);; CSV files (*.csv);; Numpy files (*.npy)"

        # folder icon
        self.folder_btn = QtWidgets.QPushButton()
        self.folder_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
        self.folder_btn.clicked.connect(self.get_file)

        # put filepath & folder icon into one grouping
        filepath_layout = QtWidgets.QHBoxLayout()
        filepath_layout.addWidget(self.filepath_input)
        filepath_layout.addWidget(self.folder_btn)

        self.setLayout(filepath_layout)

    def get_file(self):
        dlg = QtWidgets.QFileDialog(self, "Select file", directory=self.directory, filter=self.filter)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        if dlg.exec_():
            selected_file = dlg.selectedFiles()
            self.filepath = selected_file[0]
            self.filepath_input.setText(selected_file[0])


class MultiFileDialog(QtWidgets.QWidget):
    """
    Module for Qt Widget for 'Open File Dialog'
    """

    def __init__(self, *args, **kwargs):
        super(MultiFileDialog, self).__init__(*args, **kwargs)
        self.setFixedWidth(750)

        # displays selected files in list
        self.filepaths_input = QtWidgets.QTextEdit()
        self.filepaths_input.setPlaceholderText("[Selected files...]")
        self.filepaths_input.setDisabled(True)
        self.filepaths = []
        self.directory = project_root
        self.filter = "Text, CSV, or Numpy files (*.txt; *.csv; *.npy);; \
                    Text files (*.txt);; CSV files (*.csv);; Numpy files (*.npy)"

        # folder icon
        self.folder_btn = QtWidgets.QPushButton()
        self.folder_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
        self.folder_btn.clicked.connect(self.get_files)

        # put filepath & folder icon into one grouping
        filepath_layout = QtWidgets.QHBoxLayout()
        filepath_layout.addWidget(self.filepaths_input)
        filepath_layout.addWidget(self.folder_btn)

        self.setLayout(filepath_layout)

    def get_files(self):
        dlg = QtWidgets.QFileDialog(self, "Select files", directory=self.directory, filter=self.filter)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)

        if dlg.exec_():
            self.filepaths = dlg.selectedFiles()

            text_display = ""
            for f in self.filepaths:
                text_display = text_display + str(f) + "\n"

            self.filepaths_input.setText(text_display)