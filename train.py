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
    parser.add_argument('--seed', type=int, default=42,
                        help='seed number',
                        dest='seed')
    parser.add_argument('--path', type=str, default='data',
                        help='path directory that includes data',
                        dest='path')
    parser.add_argument('--name_x_forward', type=str, default='data/x_forward_1',
                        help='name of npy file that contains the forward sequences',
                        dest='name_x_forward')
    parser.add_argument('--name_x_reverse', type=str, default='data/x_reverse_1',
                        help='name of npy file that contains the reverse sequences',
                        dest='name_x_reverse')
    parser.add_argument('--name_y', type=str, default='data/x_reverse_1',
                        help='name of npy file that contains the binding values',
                        dest='name_y')

    return parser


def load_model():
    cnn: CNN = CNN()

    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    device = torch.device(dev)
    cnn.to(device)
    cnn.train()
    optim = torch.optim.SGD(cnn.parameters(), lr=1e-3, weight_decay=0.01)

    return cnn, optim


def load_data(path, name_x_forward, name_x_reverse, name_y):
    dna_seqs_for = np.load(os.path.join(path, name_x_forward))
    dna_seqs_rev = np.load(os.path.join(path, name_x_reverse))
    dna_binding_values = np.load(os.path.join(path, name_y))

    x_tensors_for = torch.tensor(dna_seqs_for).unsqueeze(1)
    print(x_tensors_for.shape)
    x_tensors_rev = torch.tensor(dna_seqs_rev).unsqueeze(1)
    y_tensors = torch.tensor(dna_binding_values).unsqueeze(1)

    dataset = TensorDataset(x_tensors_for, x_tensors_rev, y_tensors)
    train_length = int(TRAIN_SPLIT * x_tensors_for.shape[0])
    test_length = x_tensors_for.shape[0] - train_length

    train_dataset, test_dataset = random_split(dataset, [train_length, test_length])

    train_loader = DataLoader(train_dataset, batch_size=100, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=100, shuffle=True)

    return train_loader, test_loader


if __name__ == '__main__':

    args = get_parser().parse_args()

    model, optimizer = load_model()
    model = model.float()

    epochs = args.epochs
    seed = args.seed
    path = args.path
    name_x_forward = args.name_x_forward
    name_x_reverse = args.name_x_reverse
    name_y = args.name_y

    torch.manual_seed(seed)

    train_loader, test_loader = load_data(path, name_x_forward, name_x_reverse, name_y)

    # TRACKERS
    train_losses = []
    test_losses = []
    train_correct = []
    test_correct = []

    start_time = time.time()

    for epoch in range(epochs):
        trn_correct = 0
        tst_correct = 0
        for b, (X_train_forward, X_train_reverse, y_train) in enumerate(train_loader):
            b += 1
            pred = model(X_train_forward.float(), X_train_reverse.float())
            loss = model.loss(pred, y_train.float())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if b % 100 == 0:
                print(f'Epoch {epoch} batch {b} loss: {loss.item()}')
        train_losses.append(loss)

    total_time = time.time() - start_time
    print(f'Duration: {total_time / 60} mins')
    torch.save(model.state_dict(), 'model')
    np.save('train_losses.npy', train_losses)
