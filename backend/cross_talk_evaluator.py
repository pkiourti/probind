import torch
import numpy as np
from backend.cnn import CNN
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import seaborn as sns
from typing import Union
from matplotlib import colors as mcolors

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
plt.style.use('seaborn-dark')

project_root = os.environ.get('PYTHONPATH')
try:
    project_root = project_root.split(os.path.pathsep)[1]
except Exception as e:
    pass

base_idx_mapping = {'A': 0, 'T': 1, 'C': 2, 'G': 3}


class CrossTalkEvaluator(object):

    def __init__(self):
        self.dev = "cpu"
        self.model = ""
        self.model_name = ""
        self.figure = ""
        self.line1 = ""
        self.line2 = ""

    def compute_reverse_complements(self, seq_1, seq_2):
        identity_matrix = np.eye(4, dtype=int)

        reverse_1 = np.flip(
            [identity_matrix[self.complement_base(np.argmax(i))].tolist() for i in np.transpose(seq_1)], 0)

        reverse_2 = np.flip(
            [identity_matrix[self.complement_base(np.argmax(i))].tolist() for i in np.transpose(seq_2)], 0)

        return np.transpose(reverse_1), np.transpose(reverse_2)

    def load_model(self, model_name):
        self.model = CNN()

        device = torch.device(self.dev)
        self.model.to(device)
        self.model.load_state_dict(torch.load(os.path.join(project_root, 'models', model_name)))
        self.model.eval()

        self.model_name = model_name

    @staticmethod
    def complement_base(idx):
        if idx == 0:
            return 1
        elif idx == 1:
            return 0
        elif idx == 2:
            return 3
        elif idx == 3:
            return 2

    def seq_to_array(self, seq):
        list = []
        identity = np.eye(4)
        for base in seq:
            list.extend([identity[base_idx_mapping[base]].tolist()])

        return np.transpose(np.asarray(list))

    def convert_seqs_to_array(self, seq_1: Union[str, np.ndarray], seq_2: Union[str, np.ndarray]):
        seq_1 = self.seq_to_array(seq_1) if type(seq_1) == str else seq_1
        seq_2 = self.seq_to_array(seq_2) if type(seq_2) == str else seq_2

        return seq_1, seq_2

    def predict_binding(self, seq_length, x_forward, x_reverse):
        input_length = self.model.input_length
        no_of_bind_values = int(seq_length / input_length)

        bind_values = []
        for i in range(no_of_bind_values):
            start = i * input_length
            end = start + input_length
            binding = self.model.forward(x_forward[:, :, :, start: end], x_reverse[:, :, :, start: end])
            bind_values.extend([binding.item()])
        return bind_values

    def run(self, seq_1: Union[str, np.ndarray], seq_2: Union[str, np.ndarray]):

        seq_1, seq_2 = self.convert_seqs_to_array(seq_1, seq_2)

        x_reverse_1, x_reverse_2 = self.compute_reverse_complements(seq_1, seq_2)

        x_forward_1 = torch.FloatTensor(seq_1.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)
        x_forward_2 = torch.FloatTensor(seq_2.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)
        x_reverse_1 = torch.FloatTensor(x_reverse_1.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)
        x_reverse_2 = torch.FloatTensor(x_reverse_2.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)

        bind_values_1 = self.predict_binding(seq_1.shape[-1], x_forward_1, x_reverse_1)
        bind_values_2 = self.predict_binding(seq_2.shape[-1], x_forward_2, x_reverse_2)

        return bind_values_1, bind_values_2

    def integers(self, x, pos):
        return '%1d' % x

    def one_decimal(self, y, pos):
        return '%1.1f' % y

    def plot_seq_bindings(self, ax, xlim, bindings, legend, xlabel, ylabel, threshold):
        size = [i * self.model.input_length for i in range(len(bindings))]
        ax.plot(size, bindings, label=legend)
        line, = ax.plot(size, [threshold for _ in range(len(bindings))], label='threshold', color=colors['darkred'])
        ax.legend(fontsize=15)
        ax.grid()
        ax.set_ylim(0, 1.01)
        ax.set_xlim(0, xlim)
        ax.set_xticklabels(ax.get_xticks(), {'size': 13})
        ax.set_yticklabels(ax.get_yticks(), {'size': 13})
        ax.xaxis.set_major_formatter(FuncFormatter(self.integers))
        ax.yaxis.set_major_formatter(FuncFormatter(self.one_decimal))
        ax.set_ylabel(ylabel, fontsize=15)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=15)

        return line

    def plot_bindings(self, threshold, binding_1, binding_2):
        size1 = len(binding_1) * 300
        size2 = len(binding_2) * 300

        size = size1 if size1 > size2 else size2

        size = 1.01 * size

        self.figure = plt.figure(figsize=(20, 10))
        ax1 = self.figure.add_subplot(2, 1, 1)
        self.line1 = self.plot_seq_bindings(ax1, size, binding_1, 'DNA seq 1', "DNA base position", "Binding values", threshold)

        ax2 = self.figure.add_subplot(2, 1, 2)
        self.line2 = self.plot_seq_bindings(ax2, size, binding_2, 'DNA seq 2', "DNA base position", "Binding values", threshold)

        self.figure.suptitle("Cross Talk for Transcription Factor: " + str(self.model_name), fontsize=25)
        return self.figure

