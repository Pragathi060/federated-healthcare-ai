import os
import pandas as pd
from ucimlrepo import fetch_ucirepo


OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "liver"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


print("Downloading Liver Disease dataset...")


dataset = fetch_ucirepo(id=225)


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
    "liver_dataset.csv"
)


df.to_csv(
    output_path,
    index=False
)


print()
print("Saved to:")
print(output_path)