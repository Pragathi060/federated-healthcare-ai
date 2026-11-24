import os
import torch

from ml.disease_config import get_disease_config
from ml.model import DiseaseRiskModel
from ml.tb_model import create_tb_model


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)


# ============================================================
# FEDERATED MODEL FILES
# ============================================================

FEDERATED_MODEL_FILES = {

    "diabetes":
        "diabetes_federated_model.pth",

    "hypertension":
        "hypertension_federated_model.pth",

    "heart":
        "heart_federated_model.pth",

    "kidney":
        "kidney_federated_model.pth",

    "liver":
        "liver_federated_model.pth",

    "tuberculosis":
        "tb_federated_model.pth"
}


# ============================================================
# GET FEDERATED MODEL FILE
# ============================================================

def get_federated_model_file(disease):

    return FEDERATED_MODEL_FILES.get(
        disease.lower()
    )


# ============================================================
# LOAD TABULAR DISEASE MODEL
# ============================================================

def load_tabular_model(
    disease,
    use_federated=False
):

    disease = disease.lower()

    config = get_disease_config(
        disease
    )

    # --------------------------------------------------------
    # Default model
    # --------------------------------------------------------

    model_file = config[
        "model_file"
    ]

    # --------------------------------------------------------
    # Select federated model
    # --------------------------------------------------------

    if use_federated:

        federated_file = (
            get_federated_model_file(
                disease
            )
        )

        if federated_file:

            federated_path = os.path.join(
                MODELS_DIR,
                federated_file
            )

            if os.path.exists(
                federated_path
            ):

                model_file = federated_file

                print()
                print(
                    "======================================"
                )
                print(
                    f"USING FEDERATED "
                    f"{config['name'].upper()} MODEL"
                )
                print(
                    "======================================"
                )
                print(
                    federated_path
                )
                print()

            else:

                print()
                print(
                    f"Federated "
                    f"{config['name']} model not found."
                )

                print(
                    f"Using normal "
                    f"{config['name']} model."
                )

                print()

    # --------------------------------------------------------
    # Complete model path
    # --------------------------------------------------------

    model_path = os.path.join(
        MODELS_DIR,
        model_file
    )

    # --------------------------------------------------------
    # Check model exists
    # --------------------------------------------------------

    if not os.path.exists(
        model_path
    ):

        raise FileNotFoundError(
            f"Model file not found: "
            f"{model_path}"
        )

    # --------------------------------------------------------
    # Number of input features
    # --------------------------------------------------------

    input_size = len(
        config["features"]
    )

    # ========================================================
    # CREATE CORRECT MODEL ARCHITECTURE
    # ========================================================

    # --------------------------------------------------------
    # Diabetes
    # --------------------------------------------------------

    if disease == "diabetes":

        model = DiseaseRiskModel(
            input_size
        )

    # --------------------------------------------------------
    # Hypertension
    # --------------------------------------------------------

    elif disease == "hypertension":

        from ml.hypertension_model import (
            HypertensionModel
        )

        model = HypertensionModel(
            input_size=input_size,
            num_classes=3
        )

    # --------------------------------------------------------
    # Heart Disease
    # --------------------------------------------------------

    elif disease == "heart":

        from ml.heart_model import (
            HeartDiseaseModel
        )

        model = HeartDiseaseModel(
            input_size=input_size,
            num_classes=2
        )

    # --------------------------------------------------------
    # Kidney Disease
    # --------------------------------------------------------

    elif disease == "kidney":

        from ml.kidney_model import (
            KidneyDiseaseModel
        )

        model = KidneyDiseaseModel(
            input_size=input_size,
            num_classes=2
        )

    # --------------------------------------------------------
    # Liver Disease
    # --------------------------------------------------------

    elif disease == "liver":

        from ml.liver_model import (
            LiverDiseaseModel
        )

        model = LiverDiseaseModel(
            input_size=input_size,
            num_classes=2
        )

    else:

        raise ValueError(
            f"Unsupported tabular disease: "
            f"{disease}"
        )

    # ========================================================
    # LOAD MODEL PARAMETERS
    # ========================================================

    state_dict = torch.load(
        model_path,
        map_location="cpu"
    )

    model.load_state_dict(
        state_dict
    )

    model.eval()

    return model


# ============================================================
# LOAD TUBERCULOSIS CNN MODEL
# ============================================================

def load_tb_model(
    use_federated=True
):

    config = get_disease_config(
        "tuberculosis"
    )

    # --------------------------------------------------------
    # Default TB model
    # --------------------------------------------------------

    model_file = config[
        "model_file"
    ]

    # --------------------------------------------------------
    # Select federated TB model
    # --------------------------------------------------------

    if use_federated:

        federated_file = (
            get_federated_model_file(
                "tuberculosis"
            )
        )

        if federated_file:

            federated_path = os.path.join(
                MODELS_DIR,
                federated_file
            )

            if os.path.exists(
                federated_path
            ):

                model_file = federated_file

                print()
                print(
                    "======================================"
                )
                print(
                    "USING FEDERATED "
                    "TUBERCULOSIS MODEL"
                )
                print(
                    "======================================"
                )
                print(
                    federated_path
                )
                print()

            else:

                print()
                print(
                    "Federated Tuberculosis "
                    "model not found."
                )

                print(
                    "Using normal Tuberculosis model."
                )

                print()

    # --------------------------------------------------------
    # Complete model path
    # --------------------------------------------------------

    model_path = os.path.join(
        MODELS_DIR,
        model_file
    )

    # --------------------------------------------------------
    # Check model exists
    # --------------------------------------------------------

    if not os.path.exists(
        model_path
    ):

        raise FileNotFoundError(
            f"TB model file not found: "
            f"{model_path}"
        )

    # --------------------------------------------------------
    # Create TB CNN
    # --------------------------------------------------------

    model = create_tb_model()

    # --------------------------------------------------------
    # Load parameters
    # --------------------------------------------------------

    state_dict = torch.load(
        model_path,
        map_location="cpu"
    )

    model.load_state_dict(
        state_dict
    )

    model.eval()

    return model


# ============================================================
# GENERAL MODEL LOADER
# ============================================================

def load_model(
    disease,
    use_federated=True
):

    disease = disease.lower()

    config = get_disease_config(
        disease
    )

    # --------------------------------------------------------
    # Image-based disease
    # --------------------------------------------------------

    if config["type"] == "image":

        return load_tb_model(
            use_federated=use_federated
        )

    # --------------------------------------------------------
    # Tabular disease
    # --------------------------------------------------------

    return load_tabular_model(
        disease,
        use_federated=use_federated
    )