import os
import torch
from PIL import Image
from torchvision import transforms

from ml.tb_model import create_tb_model


MODEL_PATH = "models/tb_federated_model.pth"

NORMAL_DIR = "data/tuberculosis/normal"
TB_DIR = "data/tuberculosis/tb"


# Same preprocessing used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.5],
        std=[0.5]
    )
])


# Load trained CNN
model = create_tb_model()

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu"
    )
)

model.eval()


def predict_image(image_path):

    image = Image.open(image_path).convert("L")

    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():

        output = model(image_tensor)

        probabilities = torch.softmax(
            output,
            dim=1
        )

        prediction = torch.argmax(
            probabilities,
            dim=1
        ).item()

        normal_probability = probabilities[0][0].item()
        tb_probability = probabilities[0][1].item()

    if prediction == 0:
        label = "Normal"
    else:
        label = "Tuberculosis"

    return (
        label,
        normal_probability,
        tb_probability
    )


print("\n===== TB MODEL TEST =====\n")


# Test normal images
print("NORMAL IMAGES:")

normal_images = [
    file
    for file in os.listdir(NORMAL_DIR)
    if file.lower().endswith((".png", ".jpg", ".jpeg"))
][:5]


for filename in normal_images:

    path = os.path.join(
        NORMAL_DIR,
        filename
    )

    label, normal_prob, tb_prob = predict_image(path)

    print(
        f"{filename} -> {label} | "
        f"Normal: {normal_prob * 100:.2f}% | "
        f"TB: {tb_prob * 100:.2f}%"
    )


# Test TB images
print("\nTB IMAGES:")

tb_images = [
    file
    for file in os.listdir(TB_DIR)
    if file.lower().endswith((".png", ".jpg", ".jpeg"))
][:5]


for filename in tb_images:

    path = os.path.join(
        TB_DIR,
        filename
    )

    label, normal_prob, tb_prob = predict_image(path)

    print(
        f"{filename} -> {label} | "
        f"Normal: {normal_prob * 100:.2f}% | "
        f"TB: {tb_prob * 100:.2f}%"
    )


print("\n===== TEST COMPLETE =====")