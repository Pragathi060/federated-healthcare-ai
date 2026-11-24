import os
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Get project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)


# Features used by the ML model
FEATURES = [
    "Age",
    "BMI",
    "BloodPressure",
    "TotalCholesterol",
    "LDL",
    "HDL",
    "Triglycerides",
    "GlucoseMarker",
    "BloodSugar"
]

TARGET = "Outcome"


# Train one hospital model
def train_hospital_model(hospital_name):

    file_path = os.path.join(
        DATA_DIR,
        f"{hospital_name}.csv"
    )

    df = pd.read_csv(file_path)

    X = df[FEATURES]
    y = df[TARGET]

    # Split local hospital data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Create local model
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    # Train only using this hospital's data
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Save local model
    model_path = os.path.join(
        MODEL_DIR,
        f"{hospital_name}_model.pkl"
    )

    joblib.dump(model, model_path)

    print(f"{hospital_name.upper()} model trained successfully!")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Model saved: {model_path}")
    print()

    return model, len(X_train), accuracy


# Train all four hospital models
if __name__ == "__main__":

    hospitals = [
        "hospital_a",
        "hospital_b",
        "hospital_c",
        "hospital_d"
    ]

    results = []

    for hospital in hospitals:
        model, samples, accuracy = train_hospital_model(hospital)

        results.append({
            "hospital": hospital,
            "samples": samples,
            "accuracy": accuracy
        })

    print("===================================")
    print("ALL HOSPITAL MODELS TRAINED")
    print("===================================")

    for result in results:
        print(
            f"{result['hospital']}: "
            f"{result['accuracy']:.4f}"
        )