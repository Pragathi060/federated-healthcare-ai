import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "heart",
    "heart_dataset.csv"
)


FEATURES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]


TARGET = "num"


def load_heart_data():

    df = pd.read_csv(DATA_PATH)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    df = df.replace("?", np.nan)

    df = df.dropna()

    X = df[FEATURES].astype(
        np.float32
    ).values

    # 0 = No heart disease
    # 1,2,3,4 = Heart disease
    y = (
        df[TARGET].astype(int) > 0
    ).astype(np.int64).values

    return X, y


def prepare_heart_data():

    X, y = load_heart_data()

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
    ) = prepare_heart_data()

    print("-----------------------------------")
    print("HEART DISEASE DATA PREPROCESSING")
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
        "No Heart Disease:",
        int((y_train == 0).sum())
    )

    print(
        "Heart Disease:",
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