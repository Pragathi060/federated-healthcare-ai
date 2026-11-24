from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

from ml.tb_model import create_tb_model


# Dataset location
DATA_DIR = Path(
    r"C:\Users\Pragathi Thallapally\Downloads\federated-healthcare-ai-final\federated-healthcare-ai-final\backend\data\tuberculosis"
)

# Image preprocessing
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Load images from normal/ and tb/
dataset = datasets.ImageFolder(
    root=DATA_DIR,
    transform=transform
)

print("Classes:", dataset.classes)
print("Total images:", len(dataset))


# 80% training, 20% testing
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

train_dataset, test_dataset = random_split(
    dataset,
    [train_size, test_size],
    generator=torch.Generator().manual_seed(42)
)

train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=16,
    shuffle=False
)


# Create CNN
model = create_tb_model()

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

epochs = 10

print(f"Training samples: {train_size}")
print(f"Testing samples: {test_size}")
print("Starting TB CNN training...")


# Training
for epoch in range(epochs):

    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_accuracy = correct / total

    print(
        f"Epoch [{epoch + 1}/{epochs}] "
        f"Loss: {total_loss / len(train_loader):.4f} "
        f"Accuracy: {train_accuracy:.4f}"
    )


# Evaluation
model.eval()

correct = 0
total = 0

with torch.no_grad():

    for images, labels in test_loader:

        outputs = model(images)

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_accuracy = correct / total

print()
print("TB CNN TRAINING COMPLETE")
print("------------------------")
print(f"Training samples : {train_size}")
print(f"Testing samples  : {test_size}")
print(f"Test accuracy    : {test_accuracy:.4f}")


# Save model
MODEL_DIR = Path(
    r"C:\Users\Pragathi Thallapally\Downloads\federated-healthcare-ai-final\federated-healthcare-ai-final\backend\models"
)

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "tb_model.pth"

torch.save(model.state_dict(), MODEL_PATH)

print(f"Model saved to: {MODEL_PATH}")