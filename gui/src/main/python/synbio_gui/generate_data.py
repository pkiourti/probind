from backend.generator import Generator
from utils import data_files

from PyQt5 import QtWidgets
import os
import numpy as np

project_root = os.environ.get('PYTHONPATH')
try:
    project_root = project_root.split(os.path.pathsep)[1]
except Exception as e:
    pass

class GenerateDataWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(GenerateDataWidget, self).__init__(*args, **kwargs)
        # self.setFixedWidth(250)

        gen_data_btn = QtWidgets.QPushButton("Generate random data")
        gen_data_btn.clicked.connect(self.generate_data)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(gen_data_btn)
        self.setLayout(layout)

    def generate_data(self):
        alert = QtWidgets.QMessageBox()
        alert.setWindowTitle("Generate random data")
        try:
            generator = Generator(300, 10000)
            forward, reverse, binding_values = generator.create_random_dataset()
            forward_file, reverse_file, bind_v_file = data_files(os.path.join(project_root, 'data'))
            np.save(forward_file + '.npy', forward)
            np.save(reverse_file + '.npy', reverse)
            np.save(bind_v_file + '.npy', binding_values)
            alert.setText("Random data files generated.")
            alert.setIcon(QtWidgets.QMessageBox.Information)
        except Exception as e:
            alert.setText(f"Could not generate random data. {e}")
            alert.setWindowTitle("Error")
            alert.setIcon(QtWidgets.QMessageBox.Warning)

        alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
        alert.exec_()