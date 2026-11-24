import os
import sys

import flwr as fl
import numpy as np
import pandas as pd
import torch

from sklearn.model_selection import train_test_split

from ml.model import DiseaseRiskModel
from ml.deep_learning import train_model, evaluate_model


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(BACKEND_DIR, "data")


FEATURES = [
    "Age",
    "BMI",
    "BloodPressure",
    "TotalCholesterol",
    "LDL",
    "HDL",
    "Triglycerides",
    "GlucoseMarker",
    "BloodSugar"
]

TARGET = "Outcome"


class HospitalClient(fl.client.NumPyClient):

    def __init__(self, hospital_name):

        self.hospital_name = hospital_name

        file_path = os.path.join(
            DATA_DIR,
            f"{hospital_name}.csv"
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        # Load hospital data
        df = pd.read_csv(file_path)

        X = df[FEATURES].values
        y = df[TARGET].values

        # Split local hospital data
        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test
        ) = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        # Create local deep-learning model
        self.model = DiseaseRiskModel(
            input_size=len(FEATURES)
        )

        print()
        print("-----------------------------------")
        print(f"{hospital_name.upper()} CLIENT")
        print("-----------------------------------")
        print(f"Training samples: {len(self.X_train)}")
        print(f"Testing samples: {len(self.X_test)}")
        print("Model: PyTorch Deep Neural Network")

    # ------------------------------------------------
    # GET MODEL PARAMETERS
    # ------------------------------------------------

    def get_parameters(self, config):

        return [
            parameter.detach().cpu().numpy()
            for parameter in self.model.state_dict().values()
        ]

    # ------------------------------------------------
    # SET MODEL PARAMETERS
    # ------------------------------------------------

    def set_parameters(self, parameters):

        state_dict = self.model.state_dict()

        new_state_dict = {}

        for (name, old_parameter), new_parameter in zip(
            state_dict.items(),
            parameters
        ):

            new_state_dict[name] = torch.tensor(
                new_parameter,
                dtype=old_parameter.dtype
            )

        self.model.load_state_dict(
            new_state_dict
        )

    # ------------------------------------------------
    # FEDERATED TRAINING
    # ------------------------------------------------

    def fit(self, parameters, config):

        # Receive global model
        self.set_parameters(parameters)

        # Train locally
        self.model = train_model(
            self.model,
            self.X_train,
            self.y_train,
            epochs=10,
            batch_size=16,
            learning_rate=0.001
        )

        # Evaluate local training performance
        accuracy = evaluate_model(
            self.model,
            self.X_train,
            self.y_train
        )

        print(
            f"{self.hospital_name.upper()} "
            f"local training accuracy: "
            f"{accuracy:.4f}"
        )

        return (
            self.get_parameters(config),
            len(self.X_train),
            {
                "hospital": self.hospital_name,
                "accuracy": float(accuracy)
            }
        )

    # ------------------------------------------------
    # GLOBAL MODEL EVALUATION
    # ------------------------------------------------

    def evaluate(self, parameters, config):

        # Receive aggregated global model
        self.set_parameters(parameters)

        # Evaluate on local test data
        accuracy = evaluate_model(
            self.model,
            self.X_test,
            self.y_test
        )

        loss = 1.0 - accuracy

        print(
            f"{self.hospital_name.upper()} "
            f"global model test accuracy: "
            f"{accuracy:.4f}"
        )

        return (
            float(loss),
            len(self.X_test),
            {
                "hospital": self.hospital_name,
                "accuracy": float(accuracy)
            }
        )


def start_hospital(hospital_name):

    client = HospitalClient(
        hospital_name
    )

    print(
        f"Connecting {hospital_name.upper()} "
        f"to federated server..."
    )

    fl.client.start_client(
        server_address="127.0.0.1:8080",
        client=client.to_client()
    )


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage: python client.py hospital_a"
        )

        sys.exit(1)

    hospital = sys.argv[1].lower()

    valid_hospitals = [
        "hospital_a",
        "hospital_b",
        "hospital_c",
        "hospital_d"
    ]

    if hospital not in valid_hospitals:

        print("Invalid hospital name.")

        print(
            "Use: hospital_a, hospital_b, "
            "hospital_c or hospital_d"
        )

        sys.exit(1)

    start_hospital(hospital)