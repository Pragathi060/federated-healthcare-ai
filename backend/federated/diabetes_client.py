import os
import sys

# ============================================================
# ADD BACKEND TO PYTHON PATH
# ============================================================

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

from sklearn.model_selection import train_test_split

from ml.model import DiseaseRiskModel
from ml.deep_learning import (
    train_model,
    evaluate_model
)


# ============================================================
# PATHS
# ============================================================

BACKEND_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BACKEND_DIR,
    "data",
    "diabetes",
    "diabetes_dataset.csv"
)


# ============================================================
# FEATURES
# ============================================================

FEATURES = [

    "age",

    "gender",

    "polyuria",

    "polydipsia",

    "sudden_weight_loss",

    "weakness",

    "polyphagia",

    "genital_thrush",

    "visual_blurring",

    "itching",

    "irritability",

    "delayed_healing",

    "partial_paresis",

    "muscle_stiffness",

    "alopecia",

    "obesity"
]


TARGET = "class"


# ============================================================
# HOSPITAL CLIENT
# ============================================================

class DiabetesHospitalClient(
    fl.client.NumPyClient
):

    def __init__(
        self,
        hospital_name
    ):

        self.hospital_name = (
            hospital_name
        )

        print()
        print(
            "=============================================="
        )
        print(
            f" INITIALIZING {hospital_name.upper()}"
        )
        print(
            "=============================================="
        )


        # ====================================================
        # LOAD DATASET
        # ====================================================

        df = pd.read_csv(
            DATA_PATH
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
        )


        # ====================================================
        # CONVERT YES / NO FEATURES
        # ====================================================

        yes_no_columns = [

            column

            for column in FEATURES

            if column not in [
                "age",
                "gender"
            ]
        ]


        for column in yes_no_columns:

            df[column] = (

                df[column]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({
                    "yes": 1.0,
                    "no": 0.0
                })

            )


        # ====================================================
        # CONVERT GENDER
        # ====================================================

        df["gender"] = (

            df["gender"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "male": 1.0,
                "female": 0.0
            })

        )


        # ====================================================
        # CONVERT TARGET
        # ====================================================

        df[TARGET] = (

            df[TARGET]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "positive": 1.0,
                "negative": 0.0
            })

        )


        # ====================================================
        # REMOVE INVALID ROWS
        # ====================================================

        df = df.dropna().reset_index(
            drop=True
        )


        # ====================================================
        # SPLIT DATA INTO FOUR HOSPITALS
        # ====================================================

        hospital_datasets = (
            self.split_hospitals(df)
        )

        if hospital_name not in hospital_datasets:

            raise ValueError(
                f"Invalid hospital: "
                f"{hospital_name}"
            )


        hospital_df = (
            hospital_datasets[
                hospital_name
            ]
        )


        # ====================================================
        # DISPLAY HOSPITAL INFORMATION
        # ====================================================

        print(
            f"{hospital_name}: "
            f"{len(hospital_df)} records"
        )


        # ====================================================
        # FEATURES AND TARGET
        # ====================================================

        X = hospital_df[
            FEATURES
        ].values

        y = hospital_df[
            TARGET
        ].values


        # ====================================================
        # TRAIN / TEST SPLIT
        # ====================================================

        (
            X_train,
            X_test,
            y_train,
            y_test
        ) = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=42,

            stratify=y
        )


        # ====================================================
        # USE THE SAME GLOBAL SCALING CONVENTION
        # AS THE NORMAL DIABETES MODEL
        # ====================================================
        #
        # The normal Diabetes preprocessing module fits
        # StandardScaler on the complete Diabetes dataset.
        #
        # We use that same scaler here so that:
        #
        # Training input
        #        ↓
        # Federated model
        #        ↓
        # /api/predict
        #
        # all use compatible feature scaling.
        #
        # ====================================================

        from ml.diabetes_preprocess import (
            prepare_diabetes_data
        )


        (
            _,
            _,
            _,
            _,
            global_scaler
        ) = prepare_diabetes_data()


        self.scaler = global_scaler


        # ====================================================
        # SCALE LOCAL HOSPITAL DATA
        # ====================================================

        self.X_train = (
            self.scaler.transform(
                X_train
            )
        )

        self.X_test = (
            self.scaler.transform(
                X_test
            )
        )


        self.y_train = y_train
        self.y_test = y_test


        # ====================================================
        # CREATE DISEASE MLP
        # ====================================================

        self.model = DiseaseRiskModel(
            input_size=len(FEATURES)
        )


        # ====================================================
        # DISPLAY DATA INFORMATION
        # ====================================================

        print(
            f"{hospital_name}: "
            f"Training samples = "
            f"{len(self.X_train)}"
        )

        print(
            f"{hospital_name}: "
            f"Testing samples = "
            f"{len(self.X_test)}"
        )

        print(
            f"{hospital_name}: "
            f"Features = {len(FEATURES)}"
        )

        print()


    # ========================================================
    # SPLIT DATA INTO FOUR SIMULATED HOSPITALS
    # ========================================================

    @staticmethod
    def split_hospitals(df):

        df = (

            df.sample(
                frac=1,
                random_state=42
            )

            .reset_index(
                drop=True
            )

        )


        hospital_a = df.iloc[
            :130
        ].copy()


        hospital_b = df.iloc[
            130:260
        ].copy()


        hospital_c = df.iloc[
            260:390
        ].copy()


        hospital_d = df.iloc[
            390:
        ].copy()


        return {

            "hospital_a":
                hospital_a,

            "hospital_b":
                hospital_b,

            "hospital_c":
                hospital_c,

            "hospital_d":
                hospital_d
        }


    # ========================================================
    # GET MODEL PARAMETERS
    # ========================================================

    def get_parameters(
        self,
        config
    ):

        return [

            parameter
            .detach()
            .cpu()
            .numpy()

            for parameter
            in self.model.state_dict().values()

        ]


    # ========================================================
    # SET MODEL PARAMETERS
    # ========================================================

    def set_parameters(
        self,
        parameters
    ):

        state_dict = (
            self.model.state_dict()
        )

        new_state_dict = {}


        for (

            (name, old_parameter),

            new_parameter

        ) in zip(

            state_dict.items(),

            parameters

        ):

            new_state_dict[name] = (

                torch.tensor(

                    new_parameter,

                    dtype=old_parameter.dtype

                )

            )


        self.model.load_state_dict(
            new_state_dict
        )


    # ========================================================
    # LOCAL TRAINING
    # ========================================================

    def fit(
        self,
        parameters,
        config
    ):

        # ----------------------------------------------------
        # Receive global model
        # ----------------------------------------------------

        self.set_parameters(
            parameters
        )


        # ----------------------------------------------------
        # Train using local hospital data
        # ----------------------------------------------------

        self.model = train_model(

            self.model,

            self.X_train,

            self.y_train,

            epochs=20,

            batch_size=16,

            learning_rate=0.001

        )


        # ----------------------------------------------------
        # Evaluate local training
        # ----------------------------------------------------

        accuracy = evaluate_model(

            self.model,

            self.X_train,

            self.y_train

        )


        print(

            f"{self.hospital_name}: "

            f"local training accuracy = "

            f"{accuracy:.4f}"

        )


        # ----------------------------------------------------
        # Send updated parameters to server
        # ----------------------------------------------------

        return (

            self.get_parameters(
                config
            ),

            len(self.X_train),

            {

                "hospital":
                    self.hospital_name,

                "accuracy":
                    float(accuracy)

            }

        )


    # ========================================================
    # LOCAL EVALUATION
    # ========================================================

    def evaluate(
        self,
        parameters,
        config
    ):

        # ----------------------------------------------------
        # Receive global model
        # ----------------------------------------------------

        self.set_parameters(
            parameters
        )


        # ----------------------------------------------------
        # Evaluate global model locally
        # ----------------------------------------------------

        accuracy = evaluate_model(

            self.model,

            self.X_test,

            self.y_test

        )


        loss = 1.0 - accuracy


        print(

            f"{self.hospital_name}: "

            f"test accuracy = "

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


# ============================================================
# START HOSPITAL
# ============================================================

def start_hospital(
    hospital_name
):

    client = (
        DiabetesHospitalClient(
            hospital_name
        )
    )


    fl.client.start_client(

        server_address=
        "127.0.0.1:8081",

        client=client.to_client()

    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(

            "python federated\\diabetes_client.py "
            "hospital_a"

        )

        sys.exit(1)


    hospital = (

        sys.argv[1]
        .lower()

    )


    valid_hospitals = [

        "hospital_a",

        "hospital_b",

        "hospital_c",

        "hospital_d"

    ]


    if hospital not in valid_hospitals:

        print(
            "Invalid hospital name."
        )

        print(

            "Use: hospital_a, hospital_b, "
            "hospital_c or hospital_d"

        )

        sys.exit(1)


    start_hospital(
        hospital
    )