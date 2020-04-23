from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets
from train_model_module import TrainModelWidget
from manage_models import ManageModelWidget

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("EC552 TF Orthogonality Tool")
    temp_widget = QtWidgets.QWidget()

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(TrainModelWidget())
    layout.addWidget(ManageModelWidget())
    temp_widget.setLayout(layout)

    window.setCentralWidget(temp_widget)

    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)