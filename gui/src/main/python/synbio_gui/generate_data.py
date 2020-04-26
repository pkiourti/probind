from backend.create import create_random_data

from PyQt5 import QtWidgets


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
            create_random_data()
            alert.setText("Random data files generated.")
            alert.setIcon(QtWidgets.QMessageBox.Information)
        except Exception as e:
            alert.setText(f"Could not generate random data. {e}")
            alert.setWindowTitle("Error")
            alert.setIcon(QtWidgets.QMessageBox.Warning)

        alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
        alert.exec_()