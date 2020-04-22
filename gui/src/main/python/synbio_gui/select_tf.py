from PyQt5 import QtCore, QtGui, QtWidgets


TF_LIST = ['TF1', 'TF2', 'TF3']

class SelectTFDialog(QtWidgets.QWidget):
    """
    Module for Qt Widget for 'Select TF Dialog'
    """

    def __init__(self, *args, **kwargs):
        super(SelectTFDialog, self).__init__(*args, **kwargs)
        self.setFixedSize(500, 500)
        self.setWindowTitle("Select Transcription Factor")

        label = QtWidgets.QLabel("Please select a Transcription Factor from the list below...")
        tf_list = QtWidgets.QMenu(self)
        for tf in TF_LIST:
            entry = QtWidgets.QAction(tf, tf_list)
            # entry = tf_list.addAction(tf)
            entry.triggered.connect(lambda tf=tf: self.select_tf(tf))
            tf_list.addAction(entry)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget()

        self.setLayout(layout)

    def select_tf(self, selected_tf=None):
        alert = QtWidgets.QMessageBox(self)
        alert.setText("You selected TF " + str(selected_tf))
        alert.exec_()