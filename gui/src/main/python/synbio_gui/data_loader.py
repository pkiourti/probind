import utils

from PyQt5 import QtCore, QtGui, QtWidgets
from file_dialog import FileDialog, MultiFileDialog
import os
import shutil


class DataLoaderWidget(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(DataLoaderWidget, self).__init__(*args, **kwargs)

        self.setWindowTitle("Select file to load data from")
        self.setFixedHeight(300)

        # initialize args to be used later
        self.x_fwd = ""
        self.x_rev = ""
        self.y = ""

        # create widgets
        text_label = QtWidgets.QLabel("Supported file types: .csv, .txt, and .npy \
                                        \nGo to [url for github docs] for example file formats.")

        # radio buttons
        radio_btns_label = QtWidgets.QLabel("File extension")
        csv_txt_btn = QtWidgets.QRadioButton()
        csv_txt_btn.setChecked(True)
        csv_txt_btn.setText('.csv or .txt')
        npy_btn = QtWidgets.QRadioButton()
        npy_btn.setText('.npy')

        radio_btn_layout = QtWidgets.QHBoxLayout()
        radio_btn_layout.addWidget(radio_btns_label)
        radio_btn_layout.addWidget(csv_txt_btn)
        radio_btn_layout.addWidget(npy_btn)

        # filepath widget
        filepath_dialog = FileDialog()
        filepath_dialog.directory = os.path.join(filepath_dialog.directory, 'data')
        filepath_dialog.filter = "Text, CSV files (*.txt; *.csv);; Text files (*.txt);; CSV files (*.csv)"
        npy_filepaths_dialog = MultiFileDialog()
        npy_filepaths_dialog.directory = os.path.join(npy_filepaths_dialog.directory, 'data')
        npy_filepaths_dialog.filter = "Numpy files (*.npy)"
        npy_filepaths_dialog.setVisible(False)

        csv_txt_btn.toggled.connect(lambda:filepath_dialog.setVisible(True))
        csv_txt_btn.toggled.connect(lambda:npy_filepaths_dialog.setVisible(False))
        npy_btn.toggled.connect(lambda:filepath_dialog.setVisible(False))
        npy_btn.toggled.connect(lambda:npy_filepaths_dialog.setVisible(True))

        # buttons
        cancel_btn = QtWidgets.QPushButton("Cancel")
        # cancel_btn.clicked.connect(self.input_params.close)
        cancel_btn.clicked.connect(self.close)

        train_model_btn = QtWidgets.QPushButton("Train model with this data")
        # train_model_btn.clicked.connect(self.input_params.close)
        train_model_btn.clicked.connect(self.close)

        train_model_btn.clicked.connect(lambda:self.process_selected_files(inputs=[filepath_dialog.filepath, npy_filepaths_dialog.filepaths]))

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(train_model_btn)

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(text_label)
        layout.addLayout(radio_btn_layout)
        layout.addWidget(filepath_dialog)
        layout.addWidget(npy_filepaths_dialog)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.exec_()

    def process_selected_files(self, inputs):
        # check filepath extension
        if not inputs[1]: # i.e. npy_filepath_dialogs.filepaths is empty list
            file_ext = os.path.splitext(inputs[0])[1]
        else:
            file_ext = os.path.splitext(inputs[1][0])[1]

        if file_ext == ".txt":
            self.x_fwd, self.x_rev, self.y = utils.convert_txt_to_npy(inputs[0])
        elif file_ext == ".csv":
            self.x_fwd, self.x_rev, self.y = utils.convert_csv_to_npy(inputs[0])
        elif file_ext == ".npy":
            # if files are already .npy, saves to data folder
            data_path = os.path.join(utils.project_root, 'data')

            if not os.path.exists(data_path):
                os.makedirs(data_path)

            file_names = []

            for f in inputs[1]: # inputs[1] = npy_filepath_dialog.filepaths, i.e. a list of filepaths
                name = os.path.splitext(os.path.basename(f))[0]

                if not os.path.exists(os.path.join(data_path, name + ".npy")): # if the file doesn't already exist in the /data folder, then copy it over
                    # os.replace(f, os.path.join(data_path, name + ".npy"))
                    shutil.copy(f, os.path.join(data_path, name + ".npy"))
                else: # need to give them new names
                    i = 0
                    while (os.path.exists(os.path.join(data_path, name + ".npy"))):
                        name = name + "_" + str(i)
                        i += 1
                    # os.replace(f, os.path.join(data_path, name + ".npy"))
                    shutil.copy(f, os.path.join(data_path, name + ".npy"))

                file_names.append(name)

            # assumption that there are only 2 .npy files
            # and they are appropriately named x_forward_#.npy, y_#.npy
            self.x_fwd = file_names[0] + ".npy"
            self.x_rev = utils.gen_save_rev_seq(inputs[1][0])
            self.y = file_names[1] + ".npy"

