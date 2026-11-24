import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "liver",
    "liver_dataset.csv"
)


FEATURES = [
    "Age",
    "Gender",
    "TB",
    "DB",
    "Alkphos",
    "Sgpt",
    "Sgot",
    "TP",
    "ALB",
    "A/G Ratio"
]


TARGET = "Selector"


def load_liver_data():

    df = pd.read_csv(DATA_PATH)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
    )

    # Clean missing values
    df = df.replace(
        ["?", "", "NA", "null"],
        np.nan
    )

    # Convert numeric features
    numeric_features = [
        "Age",
        "TB",
        "DB",
        "Alkphos",
        "Sgpt",
        "Sgot",
        "TP",
        "ALB",
        "A/G Ratio"
    ]

    for column in numeric_features:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Encode Gender
    df["Gender"] = (
        df["Gender"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "male": 1,
            "female": 0
        })
    )

    # Convert target
    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    # Original dataset:
    # 1 = Liver Disease
    # 2 = No Liver Disease
    #
    # Convert to:
    # 1 = Liver Disease
    # 0 = No Liver Disease

    df[TARGET] = (
        df[TARGET]
        .map({
            1: 1,
            2: 0
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


def prepare_liver_data():

    X, y = load_liver_data()

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
    ) = prepare_liver_data()

    print("-----------------------------------")
    print("LIVER DISEASE DATA PREPROCESSING")
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
        "No Liver Disease:",
        int((y_train == 0).sum())
    )

    print(
        "Liver Disease:",
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