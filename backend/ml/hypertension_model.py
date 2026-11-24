import torch
import torch.nn as nn


class HypertensionModel(nn.Module):

    def __init__(self, input_size=11, num_classes=3):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),

            nn.Linear(64, 32),
            nn.ReLU(),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, num_classes)
        )

    def forward(self, x):
        return self.network(x)


def create_hypertension_model():
    return HypertensionModel(
        input_size=11,
        num_classes=3
    )