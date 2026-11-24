import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import flwr as fl
import pandas as pd
import torch
import torch.nn as nn

from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

from ml.liver_model import LiverDiseaseModel
from ml.liver_preprocess import FEATURES, TARGET


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "liver",
    "liver_dataset.csv"
)


class LiverHospitalClient(fl.client.NumPyClient):

    def __init__(self, hospital_name):

        self.hospital_name = hospital_name

        print()
        print("-----------------------------------")
        print(
            f"{hospital_name.upper()} - "
            "LIVER DISEASE CLIENT"
        )
        print("-----------------------------------")

        df = pd.read_csv(DATA_PATH)

        df.columns = (
            df.columns.astype(str)
            .str.strip()
        )

        df = df.replace(
            ["?", "", "NA", "null"],
            pd.NA
        )

        numeric_features = [
            "Age",
            "TB",
            "DB",
            "Alkphos",
            "Sgpt",
            "Sgot",
            "TP",
            "ALB",
            "A/G Ratio"
        ]

        for column in numeric_features:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        df["Gender"] = (
            df["Gender"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "male": 1,
                "female": 0
            })
        )

        df[TARGET] = pd.to_numeric(
            df[TARGET],
            errors="coerce"
        )

        df[TARGET] = df[TARGET].map({
            1: 1,
            2: 0
        })

        df = df.dropna(
            subset=FEATURES + [TARGET]
        )

        hospital_datasets = (
            self.split_hospitals(df)
        )

        if hospital_name not in hospital_datasets:
            raise ValueError("Invalid hospital name")

        hospital_df = hospital_datasets[
            hospital_name
        ]

        X = hospital_df[
            FEATURES
        ].values.astype(float)

        y = hospital_df[
            TARGET
        ].values.astype(int)

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

        self.model = LiverDiseaseModel(
            input_size=len(FEATURES),
            num_classes=2
        )

        print(
            "Local samples:",
            len(hospital_df)
        )

        print(
            "Training samples:",
            len(self.X_train)
        )

        print(
            "Testing samples:",
            len(self.X_test)
        )

        print(
            "Features:",
            len(FEATURES)
        )


    @staticmethod
    def split_hospitals(df):

        df = df.sample(
            frac=1,
            random_state=42
        ).reset_index(drop=True)

        total = len(df)
        base_size = total // 4

        hospital_a = df.iloc[
            :base_size
        ].copy()

        hospital_b = df.iloc[
            base_size:base_size * 2
        ].copy()

        hospital_c = df.iloc[
            base_size * 2:base_size * 3
        ].copy()

        hospital_d = df.iloc[
            base_size * 3:
        ].copy()

        return {
            "hospital_a": hospital_a,
            "hospital_b": hospital_b,
            "hospital_c": hospital_c,
            "hospital_d": hospital_d
        }


    def get_parameters(self, config):

        return [
            parameter.detach()
            .cpu()
            .numpy()
            for parameter
            in self.model.state_dict().values()
        ]


    def set_parameters(self, parameters):

        state_dict = self.model.state_dict()
        new_state_dict = {}

        for (
            name,
            old_parameter
        ), new_parameter in zip(
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


    def fit(self, parameters, config):

        self.set_parameters(parameters)

        print()
        print(
            f"{self.hospital_name.upper()}: "
            "Starting local training..."
        )

        X_train = torch.tensor(
            self.X_train,
            dtype=torch.float32
        )

        y_train = torch.tensor(
            self.y_train,
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

        criterion = nn.CrossEntropyLoss()

        optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=0.001
        )

        self.model.train()

        for epoch in range(10):

            for X_batch, y_batch in dataloader:

                optimizer.zero_grad()

                outputs = self.model(
                    X_batch
                )

                loss = criterion(
                    outputs,
                    y_batch
                )

                loss.backward()

                optimizer.step()

        self.model.eval()

        with torch.no_grad():

            outputs = self.model(
                X_train
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            accuracy = (
                predictions == y_train
            ).float().mean().item()

        print(
            f"{self.hospital_name.upper()} "
            f"local accuracy: "
            f"{accuracy:.4f}"
        )

        return (
            self.get_parameters(config),
            len(self.X_train),
            {
                "hospital":
                    self.hospital_name,
                "accuracy":
                    float(accuracy)
            }
        )


    def evaluate(
        self,
        parameters,
        config
    ):

        self.set_parameters(parameters)

        X_test = torch.tensor(
            self.X_test,
            dtype=torch.float32
        )

        y_test = torch.tensor(
            self.y_test,
            dtype=torch.long
        )

        self.model.eval()

        with torch.no_grad():

            outputs = self.model(
                X_test
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            accuracy = (
                predictions == y_test
            ).float().mean().item()

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
                "hospital":
                    self.hospital_name,
                "accuracy":
                    float(accuracy)
            }
        )


def start_hospital(hospital_name):

    client = LiverHospitalClient(
        hospital_name
    )

    print()
    print(
        f"Connecting {hospital_name.upper()} "
        "to Liver Disease federated server..."
    )

    fl.client.start_client(
        server_address="127.0.0.1:8085",
        client=client.to_client()
    )


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("Usage:")
        print(
            "python federated\\"
            "liver_client.py hospital_a"
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