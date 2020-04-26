from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets
from train_model_module import TrainModelWidget
from manage_models import ManageModelWidget
from runmodel import RMW
from generate_data import GenerateDataWidget

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("EC552 TF Orthogonality Tool")
    window.setFixedSize(425, 250)
    temp_widget = QtWidgets.QWidget()

    layout = QtWidgets.QVBoxLayout()
    layout.setSpacing(0)
    layout.addWidget(TrainModelWidget())
    layout.addWidget(GenerateDataWidget())
    layout.addWidget(RMW())
    layout.addWidget(ManageModelWidget())
    temp_widget.setLayout(layout)

    window.setCentralWidget(temp_widget)

    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)