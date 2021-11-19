import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import numpy as np

class basicCNN(nn.Module):

    def __init__(self):
        super().__init__()

        # input:[N, C, L] [4, 120, 1000]
        # Output: [120, 996]
        self.conv1 = nn.Conv1d(120, 120, kernel_size=5)
        self.bn = nn.BatchNorm1d(120)

        # input:[N, C, L] [4, 120, 996]
        # Output: [120, 119]
        self.pool = nn.MaxPool1d(5)

        self.conv2 = nn.Conv1d(120, 120, kernel_size=3)
        self.dropout = nn.Dropout(0.25)

        # self.conv2 = nn.Conv1d(6, 16, 5)
        self.fc1 = nn.Linear(4680, 512)
        self.fc2 = nn.Linear(512, 64)
        self.fc3 = nn.Linear(64, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.dropout(x)
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x

def predict_result(landmark):

    main_data = landmark
    main_data = torch.unsqueeze(main_data.T, 0)

    model = basicCNN()
    model.load_state_dict(torch.load('model5.pt'))
    model.eval()

    pred = model(main_data.float())
    yprob = F.softmax(pred, dim=1)
    ypred = yprob.argmax(1)

    return ypred.item()