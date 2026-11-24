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
from flwr.common import ndarrays_to_parameters

from ml.hypertension_model import HypertensionModel


INPUT_SIZE = 11
NUM_CLASSES = 3

NUM_ROUNDS = 5
MIN_CLIENTS = 4


def get_initial_parameters():

    model = HypertensionModel(
        input_size=INPUT_SIZE,
        num_classes=NUM_CLASSES
    )

    parameters = [
        parameter.detach()
        .cpu()
        .numpy()
        for parameter
        in model.state_dict().values()
    ]

    return ndarrays_to_parameters(
        parameters
    )


class HypertensionFedAvg(
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
            f"HYPERTENSION FEDERATED ROUND "
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

        (
            aggregated_parameters,
            metrics
        ) = super().aggregate_fit(
            server_round,
            results,
            failures
        )

        if aggregated_parameters is not None:

            print(
                "FedAvg aggregation completed."
            )

            print(
                "Global Hypertension "
                "MLP parameters aggregated."
            )

        return (
            aggregated_parameters,
            metrics
        )


def start_server():

    print()
    print("===================================")
    print("HYPERTENSION FEDERATED SERVER")
    print("===================================")
    print()

    print("Model: PyTorch MLP")
    print("Features:", INPUT_SIZE)
    print("Classes:", NUM_CLASSES)
    print("Algorithm: FedAvg")
    print("Hospitals:", MIN_CLIENTS)
    print("Rounds:", NUM_ROUNDS)
    print()

    print(
        "Waiting for hypertension "
        "hospital clients..."
    )

    print()

    strategy = HypertensionFedAvg(

        fraction_fit=1.0,

        fraction_evaluate=1.0,

        min_fit_clients=MIN_CLIENTS,

        min_evaluate_clients=MIN_CLIENTS,

        min_available_clients=MIN_CLIENTS,

        initial_parameters=
            get_initial_parameters()
    )

    fl.server.start_server(

        server_address="127.0.0.1:8082",

        config=fl.server.ServerConfig(
            num_rounds=NUM_ROUNDS
        ),

        strategy=strategy
    )


if __name__ == "__main__":

    start_server()