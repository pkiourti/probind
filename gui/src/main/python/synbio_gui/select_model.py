from PyQt5 import QtCore, QtGui, QtWidgets


MDOEL_LIST = ['saved_model1', 'saved_model2', 'saved_model3']

class SelectModelDialog(QtWidgets.QWidget):
    """
    Module for Qt Widget for 'Select saved model Dialog'
    """

    def __init__(self, *args, **kwargs):
        super(SelectModelDialog, self).__init__(*args, **kwargs)
        self.setFixedSize(500, 500)
        self.setWindowTitle("Select Saved Model")

        label = QtWidgets.QLabel("Please select a saved model from the list below...")
        model_list = QtWidgets.QMenu(self)
        for model in MODEL_LIST:
            entry = QtWidgets.QAction(model, model_list)
            # entry = model_list.addAction(model)
            entry.triggered.connect(lambda model=model: self.select_model(model))
            model_list.addAction(entry)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget()

        self.setLayout(layout)

    def select_model(self, selected_model=None):
        alert = QtWidgets.QMessageBox(self)
        alert.setText("You selected model " + str(selected_model))
        alert.exec_()