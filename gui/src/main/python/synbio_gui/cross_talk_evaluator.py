import torch
import numpy as np
from cnn import CNN
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import seaborn as sns
from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
plt.style.use('seaborn-dark')


class CrossTalkEvaluator(object):

    def __init__(self, model_name):
        self.model_name = model_name
        self.model = self.load_model(model_name)
        self.dev = "cuda:0" if torch.cuda.is_available else "cpu"

    def compute_reverse_complements(self, seq_1, seq_2):
        identity_matrix = np.eye(4, dtype=int)

        reverse_1 = np.flip(
            [identity_matrix[self.complement_base(np.argmax(i))].tolist() for i in np.transpose(seq_1)], 0)

        reverse_2 = np.flip(
            [identity_matrix[self.complement_base(np.argmax(i))].tolist() for i in np.transpose(seq_2)], 0)

        return np.transpose(reverse_1), np.transpose(reverse_2)

    @staticmethod
    def load_model(model_name):
        dev = "cuda:0" if torch.cuda.is_available() else "cpu"
        cnn = CNN()

        device = torch.device(dev)
        cnn.to(device)
        cnn.load_state_dict(torch.load(os.path.join('models', model_name)))
        cnn.eval()

        return cnn

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


    def run(self, seq_1, seq_2):
        x_reverse_1, x_reverse_2 = self.compute_reverse_complements(seq_1, seq_2)

        x_forward_1 = torch.FloatTensor(seq_1.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)
        x_forward_2 = torch.FloatTensor(seq_2.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)
        x_reverse_1 = torch.FloatTensor(x_reverse_1.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)
        x_reverse_2 = torch.FloatTensor(x_reverse_2.copy()).unsqueeze(0).unsqueeze(0).to(self.dev)

        length = self.model.input_length

        bind_values_1 = []
        no_of_bind_values = int(seq_1.shape[-1]/length)
        for i in range(no_of_bind_values):
            start = i * length
            end = start + length
            value = self.model.forward(x_forward_1[:, :, :, start: end], x_reverse_1[:, :, :, start: end])
            bind_values_1.extend([value.item()])

        bind_values_2 = []
        no_of_bind_values = int(seq_1.shape[-1] / length)
        for i in range(no_of_bind_values):
            start = i * length
            end = start + length
            value = self.model.forward(x_forward_2[:, :, :, start: end], x_reverse_2[:, :, :, start: end])
            bind_values_2.extend([value.item()])

        return bind_values_1, bind_values_2

    def integers(self, x, pos):
        return '%1d'%x

    def one_decimal(self, y, pos):
        return '%1.1f'%y

    def plot_bindings(self, threshold, binding_1, binding_2):
        size1 = len(binding_1) * 300
        size2 = len(binding_2) * 300

        size = size1 if size1 > size2 else size2

        size = 1.01 * size

        figure = plt.figure(figsize=(20, 10))
        ax1 = figure.add_subplot(2, 1, 1)
        size1 = [i * self.model.input_length for i in range(len(binding_1))]
        ax1.plot(size1, binding_1, label = 'DNA seq 1')
        ax1.plot(size1, [threshold for _ in range(len(binding_1))], label='threshold', color=colors['darkred'])
        ax1.legend(fontsize=15)
        ax1.grid()
        ax1.set_ylim(0, 1.01)
        ax1.set_xlim(0, size)
        ax1.set_xticklabels(ax1.get_xticks(), {'size': 13})
        ax1.set_yticklabels(ax1.get_yticks(), {'size': 13})
        ax1.xaxis.set_major_formatter(FuncFormatter(self.integers))
        ax1.yaxis.set_major_formatter(FuncFormatter(self.one_decimal))
        ax1.set_ylabel("Binding values", fontsize=15)

        ax2 = figure.add_subplot(2, 1, 2)
        size2 = [i * self.model.input_length for i in range(len(binding_2))]
        ax2.plot(size2, binding_2, label='DNA seq 2')
        ax2.plot(size2, [threshold for _ in range(len(binding_2))], label='threshold', color=colors['darkred'])
        ax2.legend(fontsize=15)
        ax2.grid()
        ax2.set_ylim(0, 1.01)
        ax2.set_xlim(0, size)
        ax2.set_xticklabels(ax2.get_xticks(), {'size': 13})
        ax2.set_yticklabels(ax2.get_yticks(), {'size': 13})
        ax2.xaxis.set_major_formatter(FuncFormatter(self.integers))
        ax2.yaxis.set_major_formatter(FuncFormatter(self.one_decimal))
        ax2.set_xlabel("DNA positions", fontsize=15)
        ax2.set_ylabel("Binding values", fontsize=15)

        #plt.title("Binding Values of " + str(self.model_name))
        return figure
