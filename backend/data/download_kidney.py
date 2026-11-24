import os
import pandas as pd
from ucimlrepo import fetch_ucirepo


OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "kidney"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


print("Downloading Kidney Disease dataset...")


dataset = fetch_ucirepo(id=336)


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


output_path = os.path.join(
    OUTPUT_DIR,
    "kidney_dataset.csv"
)


df.to_csv(
    output_path,
    index=False
)


print()
print("Saved to:")
print(output_path)
