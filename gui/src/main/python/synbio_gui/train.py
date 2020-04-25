import torch
from torch.utils.data import TensorDataset, random_split, DataLoader

import time
import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

from gui.src.main.python.synbio_gui.cnn import CNN

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
    parser.add_argument('--name_x_forward', type=str, default='x_forward_1.npy',
                        help='name of npy file that contains the forward sequences',
                        dest='name_x_forward')
    parser.add_argument('--name_x_reverse', type=str, default='x_reverse_1.npy',
                        help='name of npy file that contains the reverse sequences',
                        dest='name_x_reverse')
    parser.add_argument('--name_y', type=str, default='y_1.npy',
                        help='name of npy file that contains the binding values',
                        dest='name_y')

    return parser


def load_model(dev):
    cnn: CNN = CNN()

    device = torch.device(dev)
    cnn.to(device)
    cnn.train()
    optim = torch.optim.SGD(cnn.parameters(), lr=1e-3, weight_decay=0.01)

    return cnn, optim


def load_data(path, name_x_forward, name_x_reverse, name_y, dev):
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


if __name__ == '__main__':

    args = get_parser().parse_args()

    dev = "cuda:0" if torch.cuda.is_available() else "cpu"

    model, optimizer = load_model(dev)
    model = model.float()

    epochs = args.epochs
    seed = args.seed
    path = args.path
    name_x_forward = args.name_x_forward
    name_x_reverse = args.name_x_reverse
    name_y = args.name_y

    torch.manual_seed(seed)

    train_loader, test_loader = load_data(path, name_x_forward, name_x_reverse, name_y, dev)

    # TRACKERS
    train_losses = []
    test_losses = []

    start_time = time.time()

    for epoch in range(epochs):
        for b, (X_train_forward, X_train_reverse, y_train) in enumerate(train_loader):
            b += 1
            pred = model(X_train_forward, X_train_reverse)
            loss = model.loss(pred, y_train)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if b % 100 == 0:
                print(f'Epoch {epoch} batch {b} loss: {loss.item()}')

        train_losses.append(loss)

        # TEST
        with torch.no_grad():
            for b, (X_test_forward, X_test_reverse, y_test) in enumerate(test_loader):
                b+=1
                pred = model(X_test_forward, X_test_reverse)

        loss = model.loss(pred, y_test)
        test_losses.extend([loss])

    total_time = time.time() - start_time
    print(f'Duration: {total_time / 60} mins')
    torch.save(model.state_dict(), 'model')
    np.save('train_losses_' + str(epochs) + '.npy', train_losses)
    np.save('test_losses_' + str(epochs) + '.npy', train_losses)
    plt.plot([i for i in range(epochs)], train_losses, label='train')
    plt.plot([i for i in range(epochs)], test_losses, label='test')
    plt.legend()
    plt.savefig('results.pdf')
