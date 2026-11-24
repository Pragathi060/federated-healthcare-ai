import os
import pandas as pd


OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "hypertension"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


URL = (
    "https://data.mendeley.com/public-files/"
)


print("-----------------------------------")
print("HYPERTENSION DATASET")
print("-----------------------------------")
print()
print("The hypertension dataset will be")
print("downloaded into:")
print(OUTPUT_DIR)
print()
print("Dataset source:")
print("Mendeley Data - Hypertension data set")
print()
print("Dataset contains 14,352 anonymized")
print("records and 12 variables.")