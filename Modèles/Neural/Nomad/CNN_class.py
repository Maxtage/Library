import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.Layer1 = nn.Sequential(
            nn.Conv2d(1, 24, 5), #gère nombre d'images une puis 24    1 défini par problème, 24 dans [10;50] va optimizable, 5 taille de la matrice [2;10]
            nn.BatchNorm2d(24),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.Layer2 = nn.Sequential(
            nn.Conv2d(24, 48, 5),
            nn.BatchNorm2d(48),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.FC = nn.Linear(
            768,
            10
        )


    def forward(self, x):
        x = self.Layer1(x)
        x = self.Layer2(x)
        x = x.view(x.size(0), -1)
        x = F.log_softmax(self.FC(x))
        return x
