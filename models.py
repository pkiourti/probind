import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import MSELoss


class CNN(nn.Module):

    def __init__(self, input_channels=1, filters=16, kernel=(4,24), stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(input_channels, filters, kernel, stride)
        self.batchNorm2d = nn.BatchNorm2d(num_features=100)


    def forward(self, X):
        X = self.conv1(X)



    def loss(self, pred, actual):
        criterion = nn.MSELoss()
        return criterion(pred, actual)
