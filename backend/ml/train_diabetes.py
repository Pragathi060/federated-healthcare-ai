import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import torch

from ml.model import DiseaseRiskModel
from ml.deep_learning import train_model, evaluate_model
from ml.diabetes_preprocess import prepare_diabetes_data


MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


print("-----------------------------------")
print("DIABETES DEEP LEARNING TRAINING")
print("-----------------------------------")


# Prepare diabetes data
(
    X_train,
    X_test,
    y_train,
    y_test,
    scaler
) = prepare_diabetes_data()


# Create MLP model
model = DiseaseRiskModel(
    input_size=X_train.shape[1]
)


print("Model: PyTorch MLP")
print("Input features:", X_train.shape[1])
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print()


# Train model
model = train_model(
    model,
    X_train,
    y_train,
    epochs=50,
    batch_size=16,
    learning_rate=0.001
)


# Evaluate model
train_accuracy = evaluate_model(
    model,
    X_train,
    y_train
)

test_accuracy = evaluate_model(
    model,
    X_test,
    y_test
)


# Save model
model_path = os.path.join(
    MODEL_DIR,
    "diabetes_model.pth"
)

torch.save(
    model.state_dict(),
    model_path
)


print("-----------------------------------")
print("TRAINING COMPLETED")
print("-----------------------------------")

print(
    f"Training Accuracy: "
    f"{train_accuracy:.4f}"
)

print(
    f"Testing Accuracy: "
    f"{test_accuracy:.4f}"
)

print()
print("Model saved to:")
print(model_path)