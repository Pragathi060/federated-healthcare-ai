import torch
import torch.nn as nn


class DiseaseRiskModel(nn.Module):
    """
    Generic deep-learning model for tabular disease-risk prediction.

    The same architecture can be reused for:
    Diabetes
    Hypertension
    Heart Disease
    Kidney Disease
    Liver Disease
    """

    def __init__(self, input_size):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),

            nn.Linear(64, 32),
            nn.ReLU(),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


def create_model(input_size):
    """
    Create a new disease prediction neural network.
    """
    return DiseaseRiskModel(input_size)


def get_model_parameters(model):
    """
    Convert PyTorch model parameters into NumPy arrays.

    These parameters can later be sent to the
    federated learning server.
    """
    return [
        parameter.detach().cpu().numpy()
        for parameter in model.state_dict().values()
    ]


def set_model_parameters(model, parameters):
    """
    Load federated parameters into a PyTorch model.
    """

    state_dict = model.state_dict()

    new_state_dict = {}

    for (name, old_parameter), new_parameter in zip(
        state_dict.items(),
        parameters
    ):
        new_state_dict[name] = torch.tensor(
            new_parameter,
            dtype=old_parameter.dtype
        )

    model.load_state_dict(new_state_dict)

    return model


def predict(model, input_data):
    """
    Predict disease risk probability.
    """

    model.eval()

    with torch.no_grad():

        if not isinstance(input_data, torch.Tensor):
            input_data = torch.tensor(
                input_data,
                dtype=torch.float32
            )

        output = model(input_data)

        probability = output.squeeze().item()

    prediction = 1 if probability >= 0.5 else 0

    return prediction, probability