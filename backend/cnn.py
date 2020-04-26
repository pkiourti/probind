import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import MSELoss


class CNN(nn.Module):

    def __init__(self, input_channels=1, filters=16, kernel=(4, 24), stride=1):
        super().__init__()
        self.input_length = 300
        self.conv1 = nn.Conv2d(input_channels, filters, kernel, stride)
        self.batchNorm = nn.BatchNorm1d(num_features=64)
        self.linear1 = nn.Linear(64, 128)
        self.dropout = nn.Dropout(0.5)
        self.linear2 = nn.Linear(128, 128)
        self.output = nn.Linear(128, 1)

    def forward(self, X_forward, X_reverse):
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
        return self.output(X)

    def loss(self, pred, actual):
        criterion = MSELoss()
        return criterion(pred, actual)
