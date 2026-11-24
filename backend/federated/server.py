import os

import flwr as fl
import torch

from flwr.common import ndarrays_to_parameters

from federated.strategy import HealthcareFedAvg
from ml.model import DiseaseRiskModel


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
MODEL_DIR = os.path.join(BACKEND_DIR, "models")

NUM_ROUNDS = 5
MIN_CLIENTS = 4


def get_initial_parameters():

    model = DiseaseRiskModel(
        input_size=9
    )

    parameters = [
        parameter.detach().cpu().numpy()
        for parameter in model.state_dict().values()
    ]

    return ndarrays_to_parameters(
        parameters
    )


def start_server():

    print()
    print("===================================")
    print("FEDERATED HEALTHCARE AI SERVER")
    print("===================================")
    print()

    print("Model: PyTorch Deep Neural Network")
    print("Federated Algorithm: FedAvg")
    print(f"Required hospitals: {MIN_CLIENTS}")
    print(f"Training rounds: {NUM_ROUNDS}")
    print()

    strategy = HealthcareFedAvg(

        output_dir=MODEL_DIR,

        fraction_fit=1.0,

        fraction_evaluate=1.0,

        min_fit_clients=MIN_CLIENTS,

        min_evaluate_clients=MIN_CLIENTS,

        min_available_clients=MIN_CLIENTS,

        initial_parameters=get_initial_parameters(),

        on_fit_config_fn=lambda server_round: {
            "round": server_round
        }
    )

    print("Waiting for hospital clients...")
    print()

    fl.server.start_server(

        server_address="127.0.0.1:8080",

        config=fl.server.ServerConfig(
            num_rounds=NUM_ROUNDS
        ),

        strategy=strategy
    )


if __name__ == "__main__":
    start_server()