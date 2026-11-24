import os
import pandas as pd
from sklearn.datasets import load_diabetes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def main():
    diabetes = load_diabetes(as_frame=True)
    df = diabetes.frame.copy()

    # Educational simulation: convert the continuous target into a binary label.
    median_target = df["target"].median()
    df["Outcome"] = (df["target"] > median_target).astype(int)

    # Keep the exact project feature names used throughout the application.
    df = df[
        [
            "age",
            "bmi",
            "bp",
            "s1",
            "s2",
            "s3",
            "s4",
            "s5",
            "s6",
            "Outcome",
        ]
    ]

    df.columns = [
        "Age",
        "BMI",
        "BloodPressure",
        "TotalCholesterol",
        "LDL",
        "HDL",
        "Triglycerides",
        "GlucoseMarker",
        "BloodSugar",
        "Outcome",
    ]

    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    hospitals = [
        ("hospital_a.csv", df.iloc[:110]),
        ("hospital_b.csv", df.iloc[110:220]),
        ("hospital_c.csv", df.iloc[220:330]),
        ("hospital_d.csv", df.iloc[330:442]),
    ]

    os.makedirs(DATA_DIR, exist_ok=True)
    for filename, hospital_df in hospitals:
        hospital_df.to_csv(os.path.join(DATA_DIR, filename), index=False)

    print("Hospital datasets created successfully!")
    print(f"Output folder: {DATA_DIR}")
    for filename, hospital_df in hospitals:
        print(f"{filename}: {len(hospital_df)} records")


if __name__ == "__main__":
    main()
