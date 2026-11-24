import torch
import flwr as fl

from ml.tb_model import create_tb_model


# --------------------------------------------------
# CREATE INITIAL GLOBAL MODEL
# --------------------------------------------------

model = create_tb_model()


def get_parameters(model):

    return [
        value.detach().cpu().numpy()
        for value in model.state_dict().values()
    ]


initial_parameters = fl.common.ndarrays_to_parameters(
    get_parameters(model)
)


# --------------------------------------------------
# SAVE GLOBAL MODEL AFTER EACH ROUND
# --------------------------------------------------

class SaveModelStrategy(fl.server.strategy.FedAvg):

    def aggregate_fit(
        self,
        server_round,
        results,
        failures
    ):

        aggregated_parameters, metrics = super().aggregate_fit(
            server_round,
            results,
            failures
        )

        if aggregated_parameters is not None:

            global_model = create_tb_model()

            ndarrays = fl.common.parameters_to_ndarrays(
                aggregated_parameters
            )

            state_dict = global_model.state_dict()

            new_state_dict = {}

            for (name, old_value), new_value in zip(
                state_dict.items(),
                ndarrays
            ):

                new_state_dict[name] = torch.tensor(
                    new_value,
                    dtype=old_value.dtype
                )

            global_model.load_state_dict(
                new_state_dict
            )

            torch.save(
                global_model.state_dict(),
                "models/tb_federated_model.pth"
            )

            print()
            print(
                f"Global TB model saved after round "
                f"{server_round}"
            )

        return aggregated_parameters, metrics


# --------------------------------------------------
# METRIC AGGREGATION
# --------------------------------------------------

def weighted_average(metrics):

    total_examples = sum(
        num_examples
        for num_examples, _ in metrics
    )

    if total_examples == 0:
        return {
            "accuracy": 0.0
        }

    weighted_accuracy = sum(
        num_examples * metric["accuracy"]
        for num_examples, metric in metrics
    )

    return {
        "accuracy": weighted_accuracy / total_examples
    }


# --------------------------------------------------
# FEDAVG STRATEGY
# --------------------------------------------------

strategy = SaveModelStrategy(

    fraction_fit=1.0,

    fraction_evaluate=1.0,

    min_fit_clients=4,

    min_evaluate_clients=4,

    min_available_clients=4,

    initial_parameters=initial_parameters,

    evaluate_metrics_aggregation_fn=weighted_average
)


# --------------------------------------------------
# SERVER
# --------------------------------------------------

print()
print("======================================")
print("TUBERCULOSIS FEDERATED SERVER")
print("======================================")
print("Model: CNN")
print("Input: Chest X-ray")
print("Classes: Normal / TB")
print("Algorithm: FedAvg")
print("Hospitals: 4")
print("Rounds: 5")
print("Port: 8086")
print("Waiting for TB hospital clients...")
print()


fl.server.start_server(

    server_address="127.0.0.1:8086",

    config=fl.server.ServerConfig(
        num_rounds=5
    ),

    strategy=strategy
)


print()
print("======================================")
print("TB FEDERATED TRAINING COMPLETE")
print("======================================")
print("Global model:")
print("models/tb_federated_model.pth")