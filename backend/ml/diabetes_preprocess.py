import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "diabetes",
    "diabetes_dataset.csv"
)


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


def load_diabetes_data():

    df = pd.read_csv(DATA_PATH)

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Convert Yes/No values to numbers
    yes_no_columns = [
        column for column in FEATURES
        if column not in ["age", "gender"]
    ]

    for column in yes_no_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "yes": 1,
                "no": 0
            })
        )

    # Convert gender
    df["gender"] = (
        df["gender"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "male": 1,
            "female": 0
        })
    )

    # Convert target
    df[TARGET] = (
        df[TARGET]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "positive": 1,
            "negative": 0
        })
    )

    # Remove incomplete rows
    df = df.dropna()

    X = df[FEATURES].values.astype(np.float32)
    y = df[TARGET].values.astype(np.float32)

    return X, y


def prepare_diabetes_data():

    X, y = load_diabetes_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler
    )


if __name__ == "__main__":

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler
    ) = prepare_diabetes_data()

    print("-----------------------------------")
    print("DIABETES DATA PREPROCESSING")
    print("-----------------------------------")

    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))
    print("Number of features:", X_train.shape[1])
    print("Positive cases:", int(y_train.sum()))
    print(
        "Negative cases:",
        int(len(y_train) - y_train.sum())
    )

    print()
    print("Data type:", X_train.dtype)
    print("Preprocessing completed successfully!")