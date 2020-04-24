from PyQt5 import QtCore, QtGui, QtWidgets


class FileDialog(QtWidgets.QWidget):
    """
    Module for Qt Widget for 'Open File Dialog'
    """

    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setFixedWidth(750)

        # filepath input
        self.filepath_input = QtWidgets.QLineEdit("default filepath")

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
        dlg = QtWidgets.QFileDialog(self, "Select file", filter="Text files (*.txt);; CSV files (*.csv);; Numpy files (*.npy)")
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        if dlg.exec_():
            selected_file = dlg.selectedFiles()
            self.filepath_input.setText(selected_file[0])
