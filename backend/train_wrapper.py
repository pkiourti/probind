import torch
from torch.utils.data import TensorDataset, random_split, DataLoader

import time
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors as mcolors
from matplotlib.ticker import FuncFormatter

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
plt.style.use('seaborn-dark')

from backend.cnn import CNN

TRAIN_SPLIT = 0.8

project_root = os.environ.get('PYTHONPATH')
try:
    project_root = project_root.split(os.path.pathsep)[1]
except Exception as e:
    pass


class TrainWrapper(object):

    def __init__(self, epochs, x_forward, x_reverse, y, model_name):

        self.epochs = epochs
        self.name_x_forward = x_forward
        self.name_x_reverse = x_reverse
        self.name_y = y

        self.path = project_root
        self.seed = 42
        torch.manual_seed(self.seed)
        self.model_name = model_name
        self.trained = False

        self.train_losses = []
        self.test_losses = []

        self.dev = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model, self.optimizer = self.define_model()
        self.train_loader, self.test_loader = self.load_data(self.path,
                                                             self.name_x_forward,
                                                             self.name_x_reverse,
                                                             self.name_y)

        self.batch_idx = 0
        self.iterator = iter(self.train_loader)

    def define_model(self):
        cnn = CNN()

        device = torch.device(self.dev)
        cnn.to(device)
        cnn.train()
        optim = torch.optim.SGD(cnn.parameters(), lr=1e-3, weight_decay=0.01)

        return cnn, optim

    def load_data(self, path, name_x_forward, name_x_reverse, name_y):
        dna_seqs_for = np.load(os.path.join(path, 'data', name_x_forward))
        dna_seqs_rev = np.load(os.path.join(path, 'data', name_x_reverse))
        dna_binding_values = np.load(os.path.join(path, 'data', name_y))

        x_tensors_for = torch.FloatTensor(dna_seqs_for).unsqueeze(1).to(self.dev)
        x_tensors_rev = torch.FloatTensor(dna_seqs_rev).unsqueeze(1).to(self.dev)
        y_tensors = torch.FloatTensor(dna_binding_values).unsqueeze(1).to(self.dev)

        dataset = TensorDataset(x_tensors_for, x_tensors_rev, y_tensors)
        train_length = int(TRAIN_SPLIT * x_tensors_for.shape[0])
        test_length = x_tensors_for.shape[0] - train_length

        train_dataset, test_dataset = random_split(dataset, [train_length, test_length])

        train_loader = DataLoader(train_dataset, batch_size=100, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=100, shuffle=False)

        return train_loader, test_loader

    def save_model(self):
        models_path = os.path.join(self.path, 'models')
        if not os.path.exists(models_path):
            os.makedirs(models_path)

        filename = os.path.join(models_path, self.model_name)
        if os.path.exists(filename):
            i = 1
            while os.path.exists(filename + '_' + str(i)):
                i += 1
            torch.save(self.model.state_dict(), filename + '_' + str(i))
            print(f'Model saved at {filename}_{str(i)}')
        else:
            torch.save(self.model.state_dict(), filename)
            print(f'Model saved at {filename}')

    def get_num_batches(self):
        return len(self.train_loader)

    def set_batch_idx(self, value):
        self.batch_idx = value

    def get_batch_idx(self):
        return self.batch_idx

    def one_step_train(self, epoch):
        X_train_forward, X_train_reverse, y_train = self.iterator.next()
        pred = self.model(X_train_forward, X_train_reverse)
        loss = self.model.loss(pred, y_train)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.set_batch_idx(self.get_batch_idx() + 1)

        if self.get_batch_idx() == self.get_num_batches():
            self.train_losses.append(loss.item())

        return 'Epoch ' + str(epoch) + ' batch ' + str(self.get_batch_idx()) + ' loss: ' + str(loss.item()) + ' \n'

    def test(self):
        with torch.no_grad():
            for X_test_forward, X_test_reverse, y_test in self.test_loader:
                pred = self.model(X_test_forward, X_test_reverse)

        loss = self.model.loss(pred, y_test)
        self.test_losses.extend([loss.item()])

    def reset(self):
        self.iterator = iter(self.train_loader)
        self.set_batch_idx(0)

    # this should be called from the UI in the exact same way
    def run(self):
        start_time = time.time()
        batches = self.get_num_batches()
        for epoch in range(self.epochs):
            while self.get_batch_idx() < batches:
                self.one_step_train(epoch)
            self.test()
            self.reset()

        total_time = time.time() - start_time
        print(f'Total training time: {total_time / 60} mins')
        self.save_model()
        return self.get_figure()

    def train(self):
        start_time = time.time()

        for epoch in range(self.epochs):
            for batch_idx, (X_train_forward, X_train_reverse, y_train) in enumerate(self.train_loader):
                batch_idx += 1
                pred = self.model(X_train_forward, X_train_reverse)
                loss = self.model.loss(pred, y_train)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                print(f'Epoch {epoch} batch {batch_idx} loss: {loss.item()}')

            self.train_losses.append(loss.item())

            # TEST
            with torch.no_grad():
                for X_test_forward, X_test_reverse, y_test in self.test_loader:
                    pred = self.model(X_test_forward, X_test_reverse)

            loss = self.model.loss(pred, y_test)
            self.test_losses.extend([loss.item()])

        total_time = time.time() - start_time
        print(f'Total training time: {total_time / 60} mins')

        self.save_model()
        figure = self.get_figure()

        return figure

    def integers(self, x, pos):
        return '%1d' % x

    def one_decimal(self, y, pos):
        return '%1.1f' % y

    def get_figure(self):
        figure = plt.figure()
        ax = figure.add_subplot()
        ax.plot([i for i in range(self.epochs)], self.train_losses, label='train')
        ax.plot([i for i in range(self.epochs)], self.test_losses, label='test')
        ax.legend()
        ax.grid()
        ax.xaxis.set_major_formatter(FuncFormatter(self.integers))
        ax.yaxis.set_major_formatter(FuncFormatter(self.one_decimal))
        plt.title(f"Learning {self.model_name}'s binding behavior")#Loss throughout training epochs")
        plt.xlabel("Training epoch")
        plt.ylabel("Loss")

        return figure

    def is_trained(self):
        return self.is_trained

    def set_trained(self):
        self.trained = True
