import json
import os

import flwr as fl
import joblib
import numpy as np
import torch

from flwr.common import parameters_to_ndarrays
from ml.model import DiseaseRiskModel


FEATURE_COUNT = 9


class HealthcareFedAvg(fl.server.strategy.FedAvg):

    def __init__(self, output_dir, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.output_dir = output_dir

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

        self.round_metrics = {}

    # ------------------------------------------------
    # SAVE GLOBAL PYTORCH MODEL
    # ------------------------------------------------

    def save_global_model(
        self,
        parameters,
        server_round
    ):

        arrays = parameters_to_ndarrays(
            parameters
        )

        model = DiseaseRiskModel(
            input_size=FEATURE_COUNT
        )

        state_dict = model.state_dict()

        new_state_dict = {}

        for (name, old_parameter), array in zip(
            state_dict.items(),
            arrays
        ):

            new_state_dict[name] = torch.tensor(
                array,
                dtype=old_parameter.dtype
            )

        model.load_state_dict(
            new_state_dict
        )

        model_path = os.path.join(
            self.output_dir,
            "global_deep_learning_model.pth"
        )

        torch.save(
            model.state_dict(),
            model_path
        )

        print()
        print(
            f"Round {server_round}: "
            f"Global deep-learning model saved to:"
        )
        print(model_path)

    # ------------------------------------------------
    # FEDERATED AGGREGATION
    # ------------------------------------------------

    def aggregate_fit(
        self,
        server_round,
        results,
        failures
    ):

        if not results:

            print(
                f"Round {server_round}: "
                "No client results received."
            )

            return None, {}

        print()
        print("===================================")
        print(
            f"FEDERATED DEEP LEARNING ROUND "
            f"{server_round}"
        )
        print("===================================")

        # Display hospital results

        for client_proxy, fit_res in results:

            hospital_name = fit_res.metrics.get(
                "hospital",
                "unknown"
            )

            accuracy = fit_res.metrics.get(
                "accuracy",
                0.0
            )

            print(
                f"{hospital_name}: "
                f"training samples="
                f"{fit_res.num_examples}, "
                f"accuracy={accuracy:.4f}"
            )

        # FedAvg aggregation

        (
            aggregated_parameters,
            aggregated_metrics
        ) = super().aggregate_fit(
            server_round,
            results,
            failures
        )

        if aggregated_parameters is not None:

            print(
                f"Round {server_round}: "
                "PyTorch model parameters "
                "aggregated successfully."
            )

            self.save_global_model(
                aggregated_parameters,
                server_round
            )

        # Store round information

        self.round_metrics[
            str(server_round)
        ] = {

            "participating_hospitals":
                len(results),

            "failed_clients":
                len(failures),

            "client_metrics": [

                {
                    "hospital":
                        fit_res.metrics.get(
                            "hospital",
                            "unknown"
                        ),

                    "accuracy":
                        fit_res.metrics.get(
                            "accuracy",
                            0.0
                        ),

                    "samples":
                        fit_res.num_examples

                }

                for _, fit_res in results
            ]
        }

        # Save metrics

        metrics_path = os.path.join(
            self.output_dir,
            "federated_round_metrics.json"
        )

        with open(
            metrics_path,
            "w"
        ) as file:

            json.dump(
                self.round_metrics,
                file,
                indent=4
            )

        return (
            aggregated_parameters,
            aggregated_metrics
        )