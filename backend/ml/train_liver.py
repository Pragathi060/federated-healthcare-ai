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

from ml.liver_model import LiverDiseaseModel
from ml.liver_preprocess import prepare_liver_data


(
    X_train,
    X_test,
    y_train,
    y_test,
    scaler
) = prepare_liver_data()


X_train = torch.tensor(
    X_train,
    dtype=torch.float32
)

y_train = torch.tensor(
    y_train,
    dtype=torch.long
)

X_test = torch.tensor(
    X_test,
    dtype=torch.float32
)

y_test = torch.tensor(
    y_test,
    dtype=torch.long
)


dataset = TensorDataset(
    X_train,
    y_train
)

dataloader = DataLoader(
    dataset,
    batch_size=16,
    shuffle=True
)


model = LiverDiseaseModel(
    input_size=10,
    num_classes=2
)


criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


print("-----------------------------------")
print("LIVER DISEASE MODEL TRAINING")
print("-----------------------------------")

print(
    "Training samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)

print(
    "Features:",
    X_train.shape[1]
)

print()


model.train()

for epoch in range(50):

    total_loss = 0.0

    for X_batch, y_batch in dataloader:

        optimizer.zero_grad()

        outputs = model(
            X_batch
        )

        loss = criterion(
            outputs,
            y_batch
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    if (epoch + 1) % 10 == 0:

        print(
            f"Epoch {epoch + 1}/50 "
            f"- Loss: {total_loss:.4f}"
        )


model.eval()

with torch.no_grad():

    train_outputs = model(
        X_train
    )

    train_predictions = torch.argmax(
        train_outputs,
        dim=1
    )

    train_accuracy = (
        train_predictions == y_train
    ).float().mean().item()


    test_outputs = model(
        X_test
    )

    test_predictions = torch.argmax(
        test_outputs,
        dim=1
    )

    test_accuracy = (
        test_predictions == y_test
    ).float().mean().item()


print()

print(
    f"Training Accuracy: "
    f"{train_accuracy:.4f}"
)

print(
    f"Testing Accuracy: "
    f"{test_accuracy:.4f}"
)


MODEL_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


MODEL_PATH = os.path.join(
    MODEL_DIR,
    "liver_model.pth"
)


torch.save(
    model.state_dict(),
    MODEL_PATH
)


print()

print("Model saved to:")

print(MODEL_PATH)

print()

print(
    "Liver Disease model "
    "training completed successfully!"
)