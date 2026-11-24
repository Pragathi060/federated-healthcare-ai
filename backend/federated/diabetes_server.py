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
import torch

from flwr.common import (
    ndarrays_to_parameters,
    parameters_to_ndarrays
)

from ml.model import DiseaseRiskModel


# ============================================================
# PATHS
# ============================================================

BACKEND_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BACKEND_DIR,
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# SETTINGS
# ============================================================

INPUT_SIZE = 16

NUM_ROUNDS = 5

MIN_CLIENTS = 4

GLOBAL_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "diabetes_federated_model.pth"
)


# ============================================================
# INITIAL MODEL PARAMETERS
# ============================================================

def get_initial_parameters():

    model = DiseaseRiskModel(
        input_size=INPUT_SIZE
    )

    parameters = [
        parameter.detach().cpu().numpy()
        for parameter in model.state_dict().values()
    ]

    return ndarrays_to_parameters(
        parameters
    )


# ============================================================
# FEDERATED STRATEGY
# ============================================================

class DiabetesFedAvg(
    fl.server.strategy.FedAvg
):

    def aggregate_fit(
        self,
        server_round,
        results,
        failures
    ):

        print()
        print("===================================")
        print(
            f"DIABETES FEDERATED ROUND "
            f"{server_round}"
        )
        print("===================================")

        print(
            "Participating hospitals:",
            len(results)
        )

        print(
            "Failed clients:",
            len(failures)
        )

        # ----------------------------------------------------
        # Display hospital metrics
        # ----------------------------------------------------

        for client_proxy, fit_res in results:

            hospital = fit_res.metrics.get(
                "hospital",
                "unknown"
            )

            accuracy = fit_res.metrics.get(
                "accuracy",
                0.0
            )

            print(
                f"{hospital}: "
                f"samples={fit_res.num_examples}, "
                f"accuracy={accuracy:.4f}"
            )

        # ----------------------------------------------------
        # FedAvg aggregation
        # ----------------------------------------------------

        aggregated_parameters, metrics = (
            super().aggregate_fit(
                server_round,
                results,
                failures
            )
        )

        # ----------------------------------------------------
        # Save aggregated global model
        # ----------------------------------------------------

        if aggregated_parameters is not None:

            arrays = parameters_to_ndarrays(
                aggregated_parameters
            )

            model = DiseaseRiskModel(
                input_size=INPUT_SIZE
            )

            state_dict = model.state_dict()

            new_state_dict = {}

            for (
                (name, old_parameter),
                new_parameter
            ) in zip(
                state_dict.items(),
                arrays
            ):

                new_state_dict[name] = torch.tensor(
                    new_parameter,
                    dtype=old_parameter.dtype
                )

            model.load_state_dict(
                new_state_dict
            )

            torch.save(
                model.state_dict(),
                GLOBAL_MODEL_PATH
            )

            print()
            print(
                "FedAvg aggregation completed."
            )

            print(
                "Global Diabetes MLP saved:"
            )

            print(
                GLOBAL_MODEL_PATH
            )

        return (
            aggregated_parameters,
            metrics
        )


# ============================================================
# START SERVER
# ============================================================

def start_server():

    print()
    print("===================================")
    print(" DIABETES FEDERATED SERVER")
    print("===================================")
    print()

    print("Model: PyTorch MLP")
    print("Features:", INPUT_SIZE)
    print("Algorithm: FedAvg")
    print("Hospitals:", MIN_CLIENTS)
    print("Rounds:", NUM_ROUNDS)
    print()

    print(
        "Global model will be saved as:"
    )

    print(
        GLOBAL_MODEL_PATH
    )

    print()

    print(
        "Waiting for diabetes hospital clients..."
    )

    strategy = DiabetesFedAvg(

        fraction_fit=1.0,

        fraction_evaluate=1.0,

        min_fit_clients=MIN_CLIENTS,

        min_evaluate_clients=MIN_CLIENTS,

        min_available_clients=MIN_CLIENTS,

        initial_parameters=(
            get_initial_parameters()
        )
    )

    fl.server.start_server(

        server_address="127.0.0.1:8081",

        config=fl.server.ServerConfig(
            num_rounds=NUM_ROUNDS
        ),

        strategy=strategy
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    start_server()