from backend.train_wrapper import TrainWrapper
import utils

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from file_dialog import FileDialog, MultiFileDialog
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class TrainModelWidget(QtWidgets.QWidget):
    """
    Custom Qt Widget for synbio_project GUI.
    Container for the buttons/functions of the "train model" button and subsequent menu options.
    """

    def __init__(self, *args, **kwargs):
        super(TrainModelWidget, self).__init__(*args, **kwargs)
        # self.setFixedWidth(250)

        # initialize variables to be referenced later throughout module
        self.model_name = ""
        self.num_epochs = 0
        self.input_params = None
        self.console_output = None
        self.x_fwd, self.x_rev, self.y = (None, None, None)

        # train model main button
        train_model_btn = QtWidgets.QPushButton("Train Model")
        train_model_btn_menu = QtWidgets.QMenu()

        # add menu items
        random_data_action = QtWidgets.QAction("Use random data", self)
        random_data_action.triggered.connect(lambda:self.input_train_params(True)) # connects menu item with function
        load_data_action = QtWidgets.QAction("Load data...", self)
        load_data_action.triggered.connect(lambda:self.input_train_params(False))

        train_model_btn_menu.addAction(random_data_action)
        train_model_btn_menu.addAction(load_data_action)

        train_model_btn.setMenu(train_model_btn_menu) # associates menu with button

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(train_model_btn)
        self.setLayout(layout)

        sys.stdout = Stream(newText=self.on_update_text)

    def input_train_params(self, use_random_data=True):
        self.input_params = QtWidgets.QDialog(self)
        self.input_params.setWindowTitle("Set training parameters...")
        self.input_params.setFixedSize(450, 200)

        explanation_text = QtWidgets.QLabel("Please enter model parameters below.\
                                            Choose a name to save the model as (max 255 chars, alphanumeric only)\
                                            and the number of epochs to train the model for (int only).")
        explanation_text.setWordWrap(True)

        name_label = QtWidgets.QLabel("Model name")
        name_input = QtWidgets.QLineEdit()
        name_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9_]{0,255}"))) # only up to 255 alphanumeric chars
        name_group = QtWidgets.QHBoxLayout()
        name_group.addWidget(name_label)
        name_group.addWidget(name_input)

        epoch_label = QtWidgets.QLabel("# training epochs")
        epoch_input = QtWidgets.QLineEdit()
        epoch_input.setValidator(QtGui.QIntValidator()) # int only
        epoch_group = QtWidgets.QHBoxLayout()
        epoch_group.addWidget(epoch_label)
        epoch_group.addWidget(epoch_input)

        # buttons
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.input_params.close)

        ok_btn = QtWidgets.QPushButton("OK")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(explanation_text)
        layout.addLayout(name_group)
        layout.addLayout(epoch_group)
        layout.addLayout((button_layout))

        self.input_params.setLayout(layout)

        if not use_random_data:
            ok_btn.clicked.connect(lambda:self.check_nonempty_inputs([name_input.text(), epoch_input.text()], False))
        else:
            ok_btn.clicked.connect(lambda: self.check_nonempty_inputs([name_input.text(), epoch_input.text()]))

        self.input_params.exec_()

    # checks for non-empty model parameter inputs
    def check_nonempty_inputs(self, inputs=[], use_random_data=True):
        invalid_inputs = False

        if len(inputs) == 0:
            invalid_inputs = True
        else:
            for i in inputs:
                if i == "":
                    invalid_inputs = True
                    break # error message only appears once

        if invalid_inputs:
            alert = QtWidgets.QMessageBox()
            alert.setText("Input must be non-empty")
            alert.setWindowTitle("Invalid input")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
            alert.exec_()
        else: # inputs are valid
            self.input_params.close()
            new_name = inputs[0]
            self.num_epochs = int(inputs[1])

            name_exists = utils.check_avail_model_name(inputs[0])

            i = 1
            while(name_exists == True):
                new_name = inputs[0] + "_" + str(i)
                name_exists = utils.check_avail_model_name(new_name)
                i += 1

            self.model_name = new_name

            if use_random_data:
                self.train_model_dialog()
            else:
                self.load_data()

    def on_update_text(self, text):
        cursor = self.console_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()


    def train_model_dialog(self, random_data=True):
        # load_dialog = QtWidgets.QDialog()
        # load_dialog.setWindowTitle("Training model")
        #
        # load_dialog_layout = QtWidgets.QVBoxLayout()
        # load_dialog_layout.addWidget(QtWidgets.QLabel("Now training model..."))
        #
        # load_dialog.setLayout(load_dialog_layout)
        # load_dialog.exec_()

        if random_data:
            self.x_fwd, self.x_rev, self.y = utils.choose_random_input_data()
            input_str = "random data"
        else:
            input_str = "selected input data"

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Training model...")
        dialog.setFixedSize(600, 500)

        label = QtWidgets.QLabel("Training model using " + input_str)

        self.console_output = QtWidgets.QTextEdit()
        self.console_output.moveCursor(QtGui.QTextCursor.Start)
        self.console_output.ensureCursorVisible()
        self.console_output.setLineWrapColumnOrWidth(500)
        self.console_output.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)

        train_wrapper = TrainWrapper(self.num_epochs, self.x_fwd, self.x_rev, self.y, self.model_name)
        loss_fig = train_wrapper.train()

        plot_btn = QtWidgets.QPushButton("Plot losses")
        plot_btn.clicked.connect(lambda: self.plot_loss_figure(loss_fig))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.console_output)
        layout.addWidget(plot_btn)

        dialog.setLayout(layout)
        dialog.exec_()

        # while not train_wrapper.is_trained():
        #     continue
        #
        # if train_wrapper.is_trained():
        #     self.plot_loss_figure(loss_fig)


    def load_data(self):
        dialog = QtWidgets.QDialog(self.input_params)
        dialog.setWindowTitle("Select file to load data from")
        dialog.setFixedHeight(300)

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
        filepath_dialog.filter = "Text files (*.txt);; CSV files (*.csv)"
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
        cancel_btn.clicked.connect(self.input_params.close)
        cancel_btn.clicked.connect(dialog.close)

        train_model_btn = QtWidgets.QPushButton("Train model with this data")
        train_model_btn.clicked.connect(self.input_params.close)
        train_model_btn.clicked.connect(dialog.close)

        train_model_btn.clicked.connect(lambda:self.process_selected_files(inputs=[filepath_dialog.filepath]))

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
        dialog.setLayout(layout)

        dialog.exec_()

    def process_selected_files(self, inputs):
        # check filepath extension
        file_ext = os.path.splitext(inputs[0])[1]
        if file_ext == ".txt":
            self.x_fwd, self.x_rev, self.y = utils.convert_txt_to_npy(inputs[0])
        elif file_ext == ".csv":
            self.x_fwd, self.x_rev, self.y = utils.convert_csv_to_npy(inputs[0])
        # elif file_ext == ".npy":
        #     # if files are already .npy, saves to data folder
        #     data_path = os.path.join(os.getcwd(), 'src', 'main', 'python', 'synbio_gui', 'data')
        #
        #     if not os.path.exists(data_path):
        #         os.makedirs(data_path)
        #
        #     file_names = []
        #
        #     for f in npy_filepaths_dialog.filepaths:
        #         name = os.path.splitext(os.path.basename(os.path.join(f)))[0]
        #         file_names.append(name)
        #
        #         if not os.path.exists(os.path.join(data_path, name + ".npy")):
        #             os.replace(f, os.path.join(data_path, name + ".npy"))
        #
        #     # assumption that there are only 2 .npy files
        #     # and they are appropriately named x_forward_#.npy, y_#.npy
        #     self.x_fwd = file_names[0]
        #     self.x_rev = utils.gen_save_rev_seq(npy_filepaths_dialog.filepaths[0])
        #     self.y = file_names[1]

        self.train_model_dialog(random_data=False)


    def plot_loss_figure(self, figure):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Training Loss Plot")

        canvas = FigureCanvas(figure)

        # refresh canvas
        canvas.draw()

        ok_btn = QtWidgets.QPushButton("Ok")
        ok_btn.clicked.connect(dialog.close)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)
        layout.addWidget(ok_btn)

        dialog.setLayout(layout)
        dialog.exec_()