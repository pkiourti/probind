import torch
from torch.utils.data import TensorDataset, random_split, DataLoader

import time
import os
import numpy as np
import argparse

from models import CNN

TRAIN_SPLIT = 0.8


def get_parser():
    parser = argparse.ArgumentParser(description="Training a model for prediction the binding value of a "
                                                 "Transcription Factor to a raw DNA Sequence")
    parser.add_argument('--epochs', type=int, default=10,
                        help='number of epochs for the training',
                        dest='epochs')
    parser.add_argument('--seed', type=int, default=100,
                        help='seed number',
                        dest='seed')

    return parser


def load_model():
    cnn: CNN = CNN()

    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    device = torch.device(dev)
    cnn.to(device)
    cnn.train()
    optim = torch.optim.SGD(cnn.parameters(), lr=1e-3, weight_decay=0.01)

    return cnn, optim


def load_data(path, name_x, name_y):
    dna_seqs = np.load(os.path.join(path, name_x))
    dna_binding_values = np.load(os.path.join(path, name_y))

    x_tensors = torch.tensor(dna_seqs)
    y_tensors = torch.tensor(dna_binding_values)

    dataset = TensorDataset(x_tensors, y_tensors)
    train_length = int(TRAIN_SPLIT * x_tensors.shape[0])
    test_length = x_tensors.shape[0] - train_length

    train_dataset, test_dataset = random_split(dataset, [train_length, test_length])

    train_loader = DataLoader(train_dataset, batch_size=100, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=100, shuffle=True)

    return train_loader, test_loader


if __name__ == '__main__':

    args = get_parser().parse_args()

    model, optimizer = load_model()

    epochs = args.epochs
    seed = args.seed
    path = args.path
    name_x = args.name_x
    name_y = args.name_y

    torch.manual_seed(seed)

    train_loader, test_loader = load_data(path, name_x, name_y)

    # TRACKERS
    train_losses = []
    test_losses = []
    train_correct = []
    test_correct = []

    start_time = time.time()

    for epoch in range(epochs):
        trn_correct = 0
        tst_correct = 0
        for b, (X_train, y_train) in enumerate(train_loader):
            b += 1
            pred = model(X_train)  # reshape using view
            loss = model.loss(pred, y_train)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if b % 100 == 0:
                print(f'Epoch {epoch} batch {b} loss: {loss.item()}')
        train_losses.append(loss)

    total_time = time.time() - start_time
    print(f'Duration: {total_time / 60} mins')
