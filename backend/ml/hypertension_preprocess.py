import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "hypertension",
    "hypertension_dataset.csv"
)


FEATURES = [
    "age",
    "sex",
    "BMI",
    "Resi",
    "SBP",
    "DBP",
    "Smoking",
    "odisease",
    "creantine",
    "BUN",
    "Noofmed"
]

TARGET = "level"


def load_hypertension_data():

    df = pd.read_csv(DATA_PATH)

    # Remove extra spaces from column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
    )

    # Remove rows with missing values
    df = df.dropna()

    X = df[FEATURES].values.astype(np.float32)

    # Convert levels 1,2,3 into 0,1,2
    y = (
        df[TARGET].values.astype(np.int64) - 1
    )

    return X, y


def prepare_hypertension_data():

    X, y = load_hypertension_data()

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
    ) = prepare_hypertension_data()

    print("-----------------------------------")
    print("HYPERTENSION DATA PREPROCESSING")
    print("-----------------------------------")

    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))
    print("Number of features:", X_train.shape[1])

    print()

    print("Class distribution:")

    print(
        "Level 1:",
        int((y_train == 0).sum())
    )

    print(
        "Level 2:",
        int((y_train == 1).sum())
    )

    print(
        "Level 3:",
        int((y_train == 2).sum())
    )

    print()

    print("Data type:", X_train.dtype)
    print("Target classes:", sorted(np.unique(y_train)))

    print()
    print("Preprocessing completed successfully!")