import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from ml.model import DiseaseRiskModel


def train_model(
    model,
    X_train,
    y_train,
    epochs=20,
    batch_size=16,
    learning_rate=0.001
):
    """
    Train the neural network locally at a hospital.
    """

    X_train = torch.tensor(
        X_train,
        dtype=torch.float32
    )

    y_train = torch.tensor(
        y_train,
        dtype=torch.float32
    ).reshape(-1, 1)

    dataset = TensorDataset(
        X_train,
        y_train
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    criterion = nn.BCELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate
    )

    model.train()

    for epoch in range(epochs):

        total_loss = 0.0

        for X_batch, y_batch in dataloader:

            optimizer.zero_grad()

            predictions = model(X_batch)

            loss = criterion(
                predictions,
                y_batch
            )

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the locally trained model.
    """

    X_test = torch.tensor(
        X_test,
        dtype=torch.float32
    )

    y_test = torch.tensor(
        y_test,
        dtype=torch.float32
    )

    model.eval()

    with torch.no_grad():

        predictions = model(X_test).squeeze()

        predicted_classes = (
            predictions >= 0.5
        ).float()

        accuracy = (
            predicted_classes == y_test
        ).float().mean().item()

    return accuracy


def create_disease_model(input_size):
    """
    Create a disease-specific neural network.
    """

    return DiseaseRiskModel(input_size)