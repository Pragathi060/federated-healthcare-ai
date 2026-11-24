from pathlib import Path
import shutil

# Extracted Montgomery dataset
root = Path.home() / "Downloads" / "MontgomerySet_extracted" / "MontgomerySet"

# X-ray images
image_dir = root / "CXR_png"

# Clinical readings
clinical_dir = root / "ClinicalReadings"

# Your project TB folders
output_dir = Path(
    r"C:\Users\Pragathi Thallapally\Downloads\federated-healthcare-ai-final\federated-healthcare-ai-final\backend\data\tuberculosis"
)

normal_dir = output_dir / "normal"
tb_dir = output_dir / "tb"

normal_dir.mkdir(parents=True, exist_ok=True)
tb_dir.mkdir(parents=True, exist_ok=True)

normal_count = 0
tb_count = 0
skipped = 0

for image_path in image_dir.glob("*.png"):

    txt_path = clinical_dir / f"{image_path.stem}.txt"

    if not txt_path.exists():
        print(f"Skipped - no clinical file: {image_path.name}")
        skipped += 1
        continue

    lines = txt_path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()

    if not lines:
        print(f"Skipped - empty clinical file: {txt_path.name}")
        skipped += 1
        continue

    label = lines[-1].strip().lower()

    if label == "normal":
        destination = normal_dir
        normal_count += 1

    elif label == "abnormal":
        destination = tb_dir
        tb_count += 1

    else:
        print(f"Skipped - unknown label '{label}': {txt_path.name}")
        skipped += 1
        continue

    shutil.copy2(image_path, destination / image_path.name)

print()
print("TB DATASET ORGANIZATION COMPLETE")
print("--------------------------------")
print(f"Normal images : {normal_count}")
print(f"TB images     : {tb_count}")
print(f"Skipped       : {skipped}")
print(f"Total         : {normal_count + tb_count}")