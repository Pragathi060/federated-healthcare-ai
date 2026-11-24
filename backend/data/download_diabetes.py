import os
import pandas as pd
from ucimlrepo import fetch_ucirepo


OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "diabetes"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


print("Downloading Diabetes dataset...")

dataset = fetch_ucirepo(id=529)

X = dataset.data.features
y = dataset.data.targets

df = pd.concat(
    [X, y],
    axis=1
)

print()
print("Dataset downloaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print()
print("Columns:")
print(df.columns.tolist())
print()

output_path = os.path.join(
    OUTPUT_DIR,
    "diabetes_dataset.csv"
)

df.to_csv(
    output_path,
    index=False
)

print("Saved to:")
print(output_path)