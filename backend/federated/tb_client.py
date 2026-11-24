import sys
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import flwr as fl
from sklearn.model_selection import train_test_split

from ml.tb_model import create_tb_model


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

DATA_DIR = (
    r"C:\Users\Pragathi Thallapally\Downloads"
    r"\federated-healthcare-ai-final\federated-healthcare-ai-final"
    r"\backend\data\tuberculosis"
)

SERVER_ADDRESS = "127.0.0.1:8086"

# Hospital number passed from command line
# 0 = Hospital A
# 1 = Hospital B
# 2 = Hospital C
# 3 = Hospital D

hospital_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0

hospital_names = ["A", "B", "C", "D"]

if hospital_id not in range(4):
    raise ValueError("Hospital ID must be 0, 1, 2, or 3")


# --------------------------------------------------
# IMAGE TRANSFORMATION
# --------------------------------------------------

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

dataset = datasets.ImageFolder(
    root=DATA_DIR,
    transform=transform
)

labels = np.array(dataset.targets)

print()
print("TB FEDERATED HOSPITAL CLIENT")
print("-----------------------------")
print(f"Hospital: {hospital_names[hospital_id]}")
print(f"Total dataset images: {len(dataset)}")
print(f"Classes: {dataset.classes}")


# --------------------------------------------------
# SPLIT DATA BETWEEN 4 HOSPITALS
# --------------------------------------------------

np.random.seed(42)

all_indices = np.arange(len(dataset))

np.random.shuffle(all_indices)

hospital_splits = np.array_split(all_indices, 4)

hospital_indices = hospital_splits[hospital_id]

hospital_labels = labels[hospital_indices]


# --------------------------------------------------
# LOCAL TRAIN / TEST SPLIT
# --------------------------------------------------

train_indices, test_indices = train_test_split(
    hospital_indices,
    test_size=0.20,
    random_state=42,
    stratify=hospital_labels
)

train_dataset = Subset(dataset, train_indices)
test_dataset = Subset(dataset, test_indices)

train_loader = DataLoader(
    train_dataset,
    batch_size=8,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=8,
    shuffle=False
)

print(f"Hospital images: {len(hospital_indices)}")
print(f"Training samples: {len(train_dataset)}")
print(f"Testing samples: {len(test_dataset)}")


# --------------------------------------------------
# FEDERATED CLIENT
# --------------------------------------------------

class TBClient(fl.client.NumPyClient):

    def __init__(self):

        self.model = create_tb_model()

    # ----------------------------------------------
    # GET MODEL PARAMETERS
    # ----------------------------------------------

    def get_parameters(self, config):

        return [
            value.detach().cpu().numpy()
            for value in self.model.state_dict().values()
        ]

    # ----------------------------------------------
    # SET MODEL PARAMETERS
    # ----------------------------------------------

    def set_parameters(self, parameters):

        state_dict = self.model.state_dict()

        new_state_dict = {}

        for (name, old_value), new_value in zip(
            state_dict.items(),
            parameters
        ):

            new_state_dict[name] = torch.tensor(
                new_value,
                dtype=old_value.dtype
            )

        self.model.load_state_dict(new_state_dict)

    # ----------------------------------------------
    # LOCAL TRAINING
    # ----------------------------------------------

    def fit(self, parameters, config):

        self.set_parameters(parameters)

        self.model.train()

        criterion = nn.CrossEntropyLoss()

        optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=0.001
        )

        epochs = 3

        for epoch in range(epochs):

            total_loss = 0.0

            for images, labels_batch in train_loader:

                optimizer.zero_grad()

                outputs = self.model(images)

                loss = criterion(
                    outputs,
                    labels_batch
                )

                loss.backward()

                optimizer.step()

                total_loss += loss.item()

        print(
            f"Hospital {hospital_names[hospital_id]} "
            f"completed local training"
        )

        return (
            self.get_parameters(config),
            len(train_dataset),
            {}
        )

    # ----------------------------------------------
    # LOCAL EVALUATION
    # ----------------------------------------------

    def evaluate(self, parameters, config):

        self.set_parameters(parameters)

        self.model.eval()

        correct = 0
        total = 0

        with torch.no_grad():

            for images, labels_batch in test_loader:

                outputs = self.model(images)

                _, predicted = torch.max(
                    outputs,
                    1
                )

                total += labels_batch.size(0)

                correct += (
                    predicted == labels_batch
                ).sum().item()

        accuracy = (
            correct / total
            if total > 0
            else 0.0
        )

        print(
            f"Hospital {hospital_names[hospital_id]} "
            f"global model accuracy: {accuracy:.4f}"
        )

        return (
            float(1.0 - accuracy),
            len(test_dataset),
            {
                "accuracy": float(accuracy)
            }
        )


# --------------------------------------------------
# START CLIENT
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print("Connecting to federated server...")
    print(f"Server: {SERVER_ADDRESS}")
    print()

    client = TBClient()

    fl.client.start_client(
        server_address=SERVER_ADDRESS,
        client=client.to_client()
    )