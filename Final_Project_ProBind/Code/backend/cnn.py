import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import MSELoss


class CNN(nn.Module):
    """ CNN model for Protein-DNA binding value prediction """

    def __init__(self, input_channels=1, filters=16, kernel=(4, 24), stride=1):
        super().__init__()
        self.input_length = 300
        self.conv1 = nn.Conv2d(input_channels, filters, kernel, stride) # defines the Convolutional Layer
        self.batchNorm = nn.BatchNorm1d(num_features=64) # defines the batch normalization layer
        self.linear1 = nn.Linear(64, 128) # defines the 1st linear layer
        self.dropout = nn.Dropout(0.5) # randomly zeroes 50% of the elements of the input tensor
        self.linear2 = nn.Linear(128, 128) # defines the 2nd layer
        self.output = nn.Linear(128, 1) # gives the output value

    def forward(self, X_forward, X_reverse):
        """
        One forward pass of the input through the CNN
        :param X_forward: a numpy array of shape torch.Size([?, 1, 4, 300]) where ? is the batch_size. In our case it is 100.
        :param X_reverse: a numpy array of shape torch.Size([?, 1, 4, 300]) where ? is the batch_size. In our case it is 100.
        :return: binding_value: one torch.float between 0 and 1 that corresponds to the binding value
        """
        print(X_forward.shape)
        X_forward = self.conv1(X_forward)
        X_reverse = self.conv1(X_reverse)
        X_forward = X_forward.view(-1, 16, 277)
        X_reverse = X_reverse.view(-1, 16, 277)
        forward_max_v = F.max_pool1d(X_forward, 277, 1)
        forward_avg_v = F.avg_pool1d(X_forward, 277, 1)
        reverse_max_v = F.max_pool1d(X_reverse, 277, 1)
        reverse_avg_v = F.avg_pool1d(X_reverse, 277, 1)
        X = torch.cat((forward_max_v, forward_avg_v, reverse_max_v, reverse_avg_v), 1)
        X = X.view(-1, 64)
        X = self.batchNorm(X)
        X = self.linear1(X)
        X = self.dropout(X)
        X = self.linear2(X)

        binding_value = self.output(X)

        return torch.exp(binding_value)

    def loss(self, pred, actual):
        """
        Calculates the mean squared loss between the predicted value and the actual value.
        :param pred: a torch.float value between 0 and 1
        :param actual: a torch.float value between 0 and 1
        :return: a torch item that includes the loss calculated using the torch.nn.MSELoss criterion
        """
        mse_loss = MSELoss()
        return mse_loss(pred, actual)
