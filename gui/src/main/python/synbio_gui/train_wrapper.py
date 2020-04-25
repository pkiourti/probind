import torch
from torch.utils.data import TensorDataset, random_split, DataLoader

import time
import os
import numpy as np
import matplotlib.pyplot as plt

from cnn import CNN

TRAIN_SPLIT = 0.8


class TrainWrapper(object):

    def __init__(self, epochs, x_forward, x_reverse, y, model_name):

        self.epochs = epochs
        self.name_x_forward = x_forward
        self.name_x_reverse = x_reverse
        self.name_y = y

        self.path = os.path.join(os.getcwd(), 'src', 'main', 'python', 'synbio_gui', 'data')
        self.seed = 42
        self.model_name = model_name
        self.trained = False

    def load_model(self, dev):
        cnn = CNN()

        device = torch.device(dev)
        cnn.to(device)
        cnn.train()
        optim = torch.optim.SGD(cnn.parameters(), lr=1e-3, weight_decay=0.01)

        return cnn, optim

    def load_data(self, path, name_x_forward, name_x_reverse, name_y, dev):
        dna_seqs_for = np.load(os.path.join(path, name_x_forward))
        dna_seqs_rev = np.load(os.path.join(path, name_x_reverse))
        dna_binding_values = np.load(os.path.join(path, name_y))

        x_tensors_for = torch.FloatTensor(dna_seqs_for).unsqueeze(1).to(dev)
        x_tensors_rev = torch.FloatTensor(dna_seqs_rev).unsqueeze(1).to(dev)
        y_tensors = torch.FloatTensor(dna_binding_values).unsqueeze(1).to(dev)

        dataset = TensorDataset(x_tensors_for, x_tensors_rev, y_tensors)
        train_length = int(TRAIN_SPLIT * x_tensors_for.shape[0])
        test_length = x_tensors_for.shape[0] - train_length

        train_dataset, test_dataset = random_split(dataset, [train_length, test_length])

        train_loader = DataLoader(train_dataset, batch_size=100, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=100, shuffle=False)

        return train_loader, test_loader

    def save_model(self, model):
        if not os.path.exists('models'):
            os.makedirs('models')

        filename = os.path.join('models', self.model_name)
        if os.path.exists(filename):
            i = 1
            while os.path.exists(filename + '_' + str(i)):
                i += 1
            torch.save(model.state_dict(), filename + '_' + str(i))
        else:
            torch.save(model.state_dict(), filename)

    def train(self):
        dev = "cuda:0" if torch.cuda.is_available() else "cpu"
        model, optimizer = self.load_model(dev)
        model = model.float()
        torch.manual_seed(self.seed)

        train_loader, test_loader = self.load_data(self.path,
                                                   self.name_x_forward,
                                                   self.name_x_reverse,
                                                   self.name_y, dev)

        # TRACKERS
        train_losses = []
        test_losses = []

        start_time = time.time()

        for epoch in range(self.epochs):
            for b, (X_train_forward, X_train_reverse, y_train) in enumerate(train_loader):
                b += 1
                pred = model(X_train_forward, X_train_reverse)
                loss = model.loss(pred, y_train)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                if b % 100 == 0:
                    print(f'Epoch {epoch} batch {b} loss: {loss.item()}')

            train_losses.append(loss.item())

            # TEST
            with torch.no_grad():
                for b, (X_test_forward, X_test_reverse, y_test) in enumerate(test_loader):
                    b += 1
                    pred = model(X_test_forward, X_test_reverse)

            loss = model.loss(pred, y_test)
            test_losses.extend([loss.item()])

        total_time = time.time() - start_time
        print(f'Total training time: {total_time / 60} mins')

        self.save_model(model)
        figure = self.get_figure(train_losses, test_losses)

        return figure

    def get_figure(self, train_losses, test_losses):
        figure = plt.figure()
        ax = figure.add_subplot()
        ax.plot([i for i in range(self.epochs)], train_losses, label='train')
        ax.plot([i for i in range(self.epochs)], test_losses, label='test')
        ax.legend()
        plt.title("Loss throughout training epochs")
        plt.xlabel("epoch")
        plt.ylabel("Loss")

        return figure

    def is_trained(self):
        return self.is_trained

    def set_trained(self):
        self.trained = True
