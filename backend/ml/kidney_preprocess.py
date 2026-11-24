import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "kidney",
    "kidney_dataset.csv"
)


FEATURES = [
    "age",
    "bp",
    "sg",
    "al",
    "su",
    "bgr",
    "bu",
    "sc",
    "sod",
    "pot",
    "hemo",
    "pcv",
    "wbcc",
    "rbcc"
]


TARGET = "class"


def load_kidney_data():

    df = pd.read_csv(DATA_PATH)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    # Clean missing-value representations
    df = df.replace(
        ["?", "\t?", " \t?", ""],
        np.nan
    )

    # Convert numerical columns
    numerical_columns = [
        "age",
        "bp",
        "sg",
        "al",
        "su",
        "bgr",
        "bu",
        "sc",
        "sod",
        "pot",
        "hemo",
        "pcv",
        "wbcc",
        "rbcc"
    ]

    for column in numerical_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Convert target
    df[TARGET] = (
        df[TARGET]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "ckd": 1,
            "notckd": 0
        })
    )

    df = df.dropna(
        subset=FEATURES + [TARGET]
    )

    X = df[FEATURES].values.astype(
        np.float32
    )

    y = df[TARGET].values.astype(
        np.int64
    )

    return X, y


def prepare_kidney_data():

    X, y = load_kidney_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(
        X_train
    )

    X_test = scaler.transform(
        X_test
    )

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
    ) = prepare_kidney_data()

    print("-----------------------------------")
    print("KIDNEY DISEASE DATA PREPROCESSING")
    print("-----------------------------------")

    print(
        "Training samples:",
        len(X_train)
    )

    print(
        "Testing samples:",
        len(X_test)
    )

    print(
        "Number of features:",
        X_train.shape[1]
    )

    print()

    print("Class distribution:")

    print(
        "No CKD:",
        int((y_train == 0).sum())
    )

    print(
        "CKD:",
        int((y_train == 1).sum())
    )

    print()

    print(
        "Data type:",
        X_train.dtype
    )

    print(
        "Target classes:",
        sorted(np.unique(y_train))
    )

    print()

    print(
        "Preprocessing completed successfully!"
    )