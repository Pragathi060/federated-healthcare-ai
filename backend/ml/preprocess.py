import pandas as pd
from sklearn.model_selection import train_test_split

FEATURES = [
    "Age",
    "BMI",
    "BloodPressure",
    "TotalCholesterol",
    "LDL",
    "HDL",
    "Triglycerides",
    "GlucoseMarker",
    "BloodSugar",
]
TARGET = "Outcome"


def load_hospital_data(path):
    df = pd.read_csv(path)
    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df[required].copy()


def split_data(df, test_size=0.2, random_state=42):
    X = df[FEATURES]
    y = df[TARGET].astype(int)
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
