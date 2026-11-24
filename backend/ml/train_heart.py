import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from ml.heart_model import HeartDiseaseModel
from ml.heart_preprocess import prepare_heart_data


def train_model(
    model,
    X_train,
    y_train,
    epochs=50,
    batch_size=16,
    learning_rate=0.001
):

    X_train = torch.tensor(
        X_train,
        dtype=torch.float32
    )

    y_train = torch.tensor(
        y_train,
        dtype=torch.long
    )

    dataset = TensorDataset(
        X_train,
        y_train
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate
    )

    model.train()

    for epoch in range(epochs):

        total_loss = 0.0

        for X_batch, y_batch in dataloader:

            optimizer.zero_grad()

            outputs = model(X_batch)

            loss = criterion(
                outputs,
                y_batch
            )

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        if (epoch + 1) % 10 == 0:

            print(
                f"Epoch [{epoch + 1}/{epochs}] "
                f"Loss: "
                f"{total_loss / len(dataloader):.4f}"
            )

    return model


def evaluate_model(
    model,
    X,
    y
):

    X = torch.tensor(
        X,
        dtype=torch.float32
    )

    y = torch.tensor(
        y,
        dtype=torch.long
    )

    model.eval()

    with torch.no_grad():

        outputs = model(X)

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        accuracy = (
            predictions == y
        ).float().mean().item()

    return accuracy


def main():

    print()
    print("===================================")
    print("HEART DISEASE DEEP LEARNING TRAINING")
    print("===================================")

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler
    ) = prepare_heart_data()

    print()
    print(
        "Training samples:",
        len(X_train)
    )

    print(
        "Testing samples:",
        len(X_test)
    )

    print(
        "Input features:",
        X_train.shape[1]
    )

    print(
        "Number of classes:",
        2
    )

    model = HeartDiseaseModel(
        input_size=X_train.shape[1],
        num_classes=2
    )

    print()
    print("Training model...")

    model = train_model(
        model,
        X_train,
        y_train,
        epochs=50,
        batch_size=16,
        learning_rate=0.001
    )

    train_accuracy = evaluate_model(
        model,
        X_train,
        y_train
    )

    test_accuracy = evaluate_model(
        model,
        X_test,
        y_test
    )

    print()
    print("===================================")
    print("TRAINING RESULTS")
    print("===================================")

    print(
        f"Training Accuracy: "
        f"{train_accuracy:.4f}"
    )

    print(
        f"Testing Accuracy: "
        f"{test_accuracy:.4f}"
    )

    model_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "models",
        "heart_model.pth"
    )

    torch.save(
        model.state_dict(),
        model_path
    )

    print()
    print("Model saved to:")
    print(model_path)

    print()
    print(
        "Heart Disease deep-learning "
        "training completed successfully!"
    )


if __name__ == "__main__":
    main()