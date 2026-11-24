from flask import Blueprint, request, jsonify

from nlp.processor import analyze_report
from nlp.disease_inference import infer_possible_diseases
from llm.assistant import generate_clinical_explanation

import os
import sys
import json
import subprocess
import joblib
import numpy as np
import pandas as pd
import torch
from PIL import Image
from torchvision import transforms

from ml.model_loader import load_model
from ml.model_loader import load_tb_model
from ml.disease_config import get_disease_config

api = Blueprint("api", __name__)


# ============================================================
# HEALTH CHECK
# ============================================================

@api.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "success",
        "message": "Federated Healthcare AI backend is running"
    })


# ============================================================
# HOSPITAL NODES
# ============================================================

@api.route("/api/hospitals", methods=["GET"])
def get_hospitals():

    hospitals = [
        {
            "id": "hospital_a",
            "name": "Hospital A",
            "status": "Connected",
            "data": "Local data",
            "model": "Local ML model",
            "records": 110
        },
        {
            "id": "hospital_b",
            "name": "Hospital B",
            "status": "Connected",
            "data": "Local data",
            "model": "Local ML model",
            "records": 110
        },
        {
            "id": "hospital_c",
            "name": "Hospital C",
            "status": "Connected",
            "data": "Local data",
            "model": "Local ML model",
            "records": 110
        },
        {
            "id": "hospital_d",
            "name": "Hospital D",
            "status": "Connected",
            "data": "Local data",
            "model": "Local ML model",
            "records": 112
        }
    ]

    return jsonify({
        "status": "success",
        "hospitals": hospitals,
        "raw_data_shared": False,
        "message": "Hospital nodes are operating locally."
    })


# ============================================================
# NLP + LLM MEDICAL REPORT ANALYSIS
# ============================================================

@api.route("/api/analyze", methods=["POST"])
@api.route("/api/nlp/analyze", methods=["POST"])
def analyze_patient_report():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "status": "error",
            "message": "Medical report text is required"
        }), 400

    report = data["text"]

    if not report.strip():
        return jsonify({
            "status": "error",
            "message": "Medical report cannot be empty"
        }), 400

    nlp_result = analyze_report(report)

    # Infer possible disease indicators from NLP findings
    disease_predictions = infer_possible_diseases(
        report,
        nlp_result
    )

    # Keep the existing LLM explanation
    explanation = generate_clinical_explanation(
        report,
        nlp_result
    )

    return jsonify({
        "status": "success",
        "nlp_analysis": nlp_result,
        "disease_predictions": disease_predictions,
        "llm_explanation": explanation,
        "disclaimer":
            "This system is for educational and research "
            "purposes only and is not a medical diagnosis."
    })

# ============================================================
# AI CLINICAL ASSISTANT
# ============================================================

@api.route("/api/llm/explain", methods=["POST"])
def llm_explain():

    data = request.get_json()

    if not data or "text" not in data:

        return jsonify({
            "status": "error",
            "error": "Text is required"
        }), 400

    report = data["text"]

    if not report.strip():

        return jsonify({
            "status": "error",
            "error": "Text cannot be empty"
        }), 400

    try:

        nlp_result = analyze_report(report)

        explanation = generate_clinical_explanation(
            report,
            nlp_result
        )

        return jsonify({

            "status": "success",

            "explanation": explanation,

            "disclaimer":
                "This system is for educational and research "
                "purposes only and is not a medical diagnosis."
        })

    except Exception as error:

        return jsonify({
            "status": "error",
            "error": str(error)
        }), 500


# ============================================================
# MULTI-DISEASE DEEP LEARNING PREDICTION
# ============================================================

@api.route("/api/predict", methods=["POST"])
def predict_disease():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Prediction data is required"
        }), 400

    try:

        # ====================================================
        # GET DISEASE
        # ====================================================

        disease = data.get("disease")

        if not disease:

            return jsonify({
                "status": "error",
                "message": "Disease is required"
            }), 400

        disease = str(disease).strip().lower()

        supported_diseases = [
            "diabetes",
            "hypertension",
            "heart",
            "kidney",
            "liver",
            "tuberculosis"
        ]

        if disease not in supported_diseases:

            return jsonify({
                "status": "error",
                "message":
                    f"Unsupported disease: {disease}",
                "supported_diseases":
                    supported_diseases
            }), 400

        # ====================================================
        # TUBERCULOSIS
        # ====================================================
        #
        # TB uses a CNN and requires a chest X-ray image.
        # The normal /api/predict endpoint is for tabular
        # diseases. A separate image endpoint will be added.
        #

        if disease == "tuberculosis":

            return jsonify({
                "status": "error",
                "message":
                    "Tuberculosis prediction requires "
                    "a chest X-ray image. "
                    "Use the TB image prediction endpoint."
            }), 400

        # ====================================================
        # DISEASE CONFIGURATION
        # ====================================================

        config = get_disease_config(disease)

        features = config["features"]

        # ====================================================
        # GET FEATURE DATA
        # ====================================================

        if (
            "features" in data
            and isinstance(data["features"], dict)
        ):

            feature_data = data["features"]

        else:

            feature_data = data

        # ====================================================
        # CHECK MISSING FEATURES
        # ====================================================

        missing_features = [
            feature
            for feature in features
            if feature not in feature_data
        ]

        if missing_features:

            return jsonify({
                "status": "error",
                "message": "Missing feature(s)",
                "missing_features": missing_features
            }), 400

        # ====================================================
        # VALUE CONVERSION
        # ====================================================

        def convert_value(value):

            if isinstance(value, str):

                value = value.strip().lower()

                # Yes / No
                if value == "yes":
                    return 1.0

                if value == "no":
                    return 0.0

                # Male / Female
                if value == "male":
                    return 1.0

                if value == "female":
                    return 0.0

                # Common categorical values
                if value == "true":
                    return 1.0

                if value == "false":
                    return 0.0

            return float(value)

        try:

            values = [
                convert_value(
                    feature_data[feature]
                )
                for feature in features
            ]

        except (TypeError, ValueError):

            return jsonify({
                "status": "error",
                "message":
                    "One or more feature values are invalid."
            }), 400

        # ====================================================
        # LOAD THE SAME STANDARD SCALER USED DURING TRAINING
        # ====================================================

        if disease == "diabetes":

            from ml.diabetes_preprocess import (
                prepare_diabetes_data
            )

            (
                _,
                _,
                _,
                _,
                scaler
            ) = prepare_diabetes_data()

        elif disease == "hypertension":

            from ml.hypertension_preprocess import (
                prepare_hypertension_data
            )

            (
                _,
                _,
                _,
                _,
                scaler
            ) = prepare_hypertension_data()

        elif disease == "heart":

            from ml.heart_preprocess import (
                prepare_heart_data
            )

            (
                _,
                _,
                _,
                _,
                scaler
            ) = prepare_heart_data()

        elif disease == "kidney":

            from ml.kidney_preprocess import (
                prepare_kidney_data
            )

            (
                _,
                _,
                _,
                _,
                scaler
            ) = prepare_kidney_data()

        elif disease == "liver":

            from ml.liver_preprocess import (
                prepare_liver_data
            )

            (
                _,
                _,
                _,
                _,
                scaler
            ) = prepare_liver_data()

        # ====================================================
        # SCALE INPUT
        # ====================================================

        input_array = np.array(
            [values],
            dtype=np.float32
        )

        scaled_input = scaler.transform(
            input_array
        )

        input_tensor = torch.tensor(
            scaled_input,
            dtype=torch.float32
        )

        # ====================================================
        # LOAD TRAINED DEEP LEARNING MODEL
        # ====================================================

        model = load_model(
            disease,
            use_federated=True
        )
        model.eval()

        # ====================================================
        # DIABETES MODEL
        # ====================================================
        #
        # Diabetes model has:
        #
        # Linear -> ReLU -> ... -> Linear(1) -> Sigmoid
        #
        # Therefore it returns one probability directly.
        #

        if disease == "diabetes":

            with torch.no_grad():

                output = model(
                    input_tensor
                )

                probability = float(
                    output.squeeze().item()
                )

            prediction = (
                1
                if probability >= 0.5
                else 0
            )

        # ====================================================
        # OTHER TABULAR MODELS
        # ====================================================
        #
        # Hypertension, Heart, Kidney and Liver models
        # return class logits.
        #

        else:

            with torch.no_grad():

                output = model(
                    input_tensor
                )

                probabilities = torch.softmax(
                    output,
                    dim=1
                )

                prediction = int(
                    torch.argmax(
                        probabilities,
                        dim=1
                    ).item()
                )

                probability = float(
                    probabilities[
                        0,
                        prediction
                    ].item()
                )

        # ====================================================
        # DISEASE-SPECIFIC LABELS
        # ====================================================

        if disease == "diabetes":

            labels = {
                0: "Negative",
                1: "Positive"
            }

            prediction_label = labels[
                prediction
            ]

        elif disease == "hypertension":

            labels = {
                0: "Level 1",
                1: "Level 2",
                2: "Level 3"
            }

            prediction_label = labels[
                prediction
            ]

        elif disease == "heart":

            labels = {
                0: "No Heart Disease",
                1: "Heart Disease"
            }

            prediction_label = labels[
                prediction
            ]

        elif disease == "kidney":

            labels = {
                0: "No CKD",
                1: "CKD"
            }

            prediction_label = labels[
                prediction
            ]

        elif disease == "liver":

            labels = {
                0: "No Liver Disease",
                1: "Liver Disease"
            }

            prediction_label = labels[
                prediction
            ]

        # ====================================================
        # RISK DESCRIPTION
        # ====================================================

        if disease == "hypertension":

            if prediction == 0:
                risk = "Lower Risk"
            else:
                risk = "Higher Risk"

        elif prediction == 0:

            risk = "Lower Risk"

        else:

            risk = "Higher Risk"

        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "status": "success",

            "disease": config["name"],

            "prediction": prediction,

            "prediction_label":
                prediction_label,

            "risk": risk,

            "probability": round(
                probability,
                4
            ),

            "percentage": round(
                probability * 100,
                2
            ),

            "model":
                config["model_type"],

            "method":
                "Federated Deep Learning"
                if disease == "diabetes"
                else "Deep Learning",

            "federated":
                disease == "diabetes",

            "disclaimer":
                "This prediction is an educational "
                "and research prototype and is not "
                "a medical diagnosis."
        })

    except KeyError as error:

        return jsonify({

            "status": "error",

            "message":
                f"Missing feature: {error}"

        }), 400

    except ValueError as error:

        return jsonify({

            "status": "error",

            "message":
                f"Invalid feature value: {error}"

        }), 400

    except FileNotFoundError as error:

        return jsonify({

            "status": "error",

            "message":
                str(error)

        }), 404

    except Exception as error:

        return jsonify({

            "status": "error",

            "message":
                str(error)

        }), 500
# ============================================================
# TUBERCULOSIS CHEST X-RAY PREDICTION
# ============================================================

@api.route("/api/predict/tuberculosis", methods=["POST"])
def predict_tuberculosis():

    if "image" not in request.files:
        return jsonify({
            "status": "error",
            "message": "Chest X-ray image is required."
        }), 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No image selected."
        }), 400

    try:

        # ====================================================
        # LOAD IMAGE
        # ====================================================

        image = Image.open(
            image_file.stream
        ).convert("L")

        # ====================================================
        # IMAGE PREPROCESSING
        # ====================================================

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.5,),
                (0.5,)
            )
        ])

        image_tensor = transform(image)

        image_tensor = image_tensor.unsqueeze(0)

        # ====================================================
        # LOAD FEDERATED TB CNN MODEL
        # ====================================================

        model = load_tb_model(
            use_federated=True
        )

        model.eval()

        # ====================================================
        # PREDICTION
        # ====================================================

        with torch.no_grad():

            output = model(
                image_tensor
            )

            probabilities = torch.softmax(
                output,
                dim=1
            )

            prediction = int(
                torch.argmax(
                    probabilities,
                    dim=1
                ).item()
            )

            probability = float(
                probabilities[
                    0,
                    prediction
                ].item()
            )

        # ====================================================
        # TB LABELS
        # ====================================================

        labels = {
            0: "Normal",
            1: "Tuberculosis"
        }

        prediction_label = labels[
            prediction
        ]

        if prediction == 0:
            risk = "Lower Risk"
        else:
            risk = "Higher Risk"

        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "status": "success",

            "disease":
                "Tuberculosis",

            "prediction":
                prediction,

            "prediction_label":
                prediction_label,

            "risk":
                risk,

            "probability":
                round(
                    probability,
                    4
                ),

            "percentage":
                round(
                    probability * 100,
                    2
                ),

            "model":
                "CNN",

            "method":
                "Federated Deep Learning",

            "federated":
                True,

            "disclaimer":
                "This prediction is an educational "
                "and research prototype and is not "
                "a medical diagnosis."
        })

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

# ============================================================
# FEDERATED LEARNING STATUS
# ============================================================

def get_federated_status():

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    model_dir = os.path.join(
        base_dir,
        "models"
    )

    metrics_path = os.path.join(
        model_dir,
        "model_metrics.json"
    )

    # Current federated model files
    federated_models = [
        "diabetes_federated_model.pth",
        "hypertension_federated_model.pth",
        "heart_federated_model.pth",
        "kidney_federated_model.pth",
        "liver_federated_model.pth",
        "tb_federated_model.pth"
    ]

    available_models = []

    for model_file in federated_models:

        model_path = os.path.join(
            model_dir,
            model_file
        )

        if os.path.exists(model_path):
            available_models.append(
                model_file
            )

    # Load metrics if available
    metrics = {}

    if os.path.exists(metrics_path):

        try:

            with open(
                metrics_path,
                "r"
            ) as file:

                metrics = json.load(file)

        except Exception:
            metrics = {}

    # No federated models found
    if not available_models:

        return jsonify({

            "status": "success",

            "available": False,

            "message":
                "Federated models have not been trained yet.",

            "method":
                "FedAvg",

            "hospitals":
                4,

            "models":
                [],

            "metrics":
                metrics
        })

    # Federated models are available
    return jsonify({

        "status": "success",

        "available": True,

        "message":
            "Federated models are available.",

        "method":
            "FedAvg",

        "hospitals":
            4,

        "models":
            available_models,

        "metrics":
            metrics
    })

@api.route(
    "/api/federated/status",
    methods=["GET"]
)
def federated_status():

    return get_federated_status()


# ============================================================
# ALTERNATIVE FEDERATED STATUS ENDPOINT
# ============================================================

@api.route(
    "/api/federated-training/status",
    methods=["GET"]
)
def federated_training_status():

    return get_federated_status()


# ============================================================
# START FEDERATED TRAINING
# ============================================================

def start_federated_training():

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    federated_dir = os.path.join(
        base_dir,
        "federated"
    )

    script_path = os.path.join(
        federated_dir,
        "run_federated.py"
    )

    if not os.path.exists(
        script_path
    ):

        return jsonify({

            "status": "error",

            "message":
                "Federated training script not found."
        }), 500

    try:

        result = subprocess.run(

            [
                sys.executable,
                script_path
            ],

            cwd=federated_dir,

            capture_output=True,

            text=True
        )

        if result.returncode != 0:

            return jsonify({

                "status": "error",

                "message":
                    "Federated training failed.",

                "error":
                    result.stderr
            }), 500

        metrics_path = os.path.join(

            base_dir,

            "models",

            "model_metrics.json"
        )

        metrics = {}

        if os.path.exists(
            metrics_path
        ):

            with open(
                metrics_path,
                "r"
            ) as file:

                metrics = json.load(
                    file
                )

        return jsonify({

            "status": "success",

            "message":
                "Federated training completed successfully.",

            "method": "FedAvg",

            "hospitals": 4,

            "metrics": metrics,

            "training_output":
                result.stdout,

            "disclaimer":
                "This is an academic federated learning "
                "simulation using simulated hospital data."
        })

    except Exception as error:

        return jsonify({

            "status": "error",

            "message":
                str(error)
        }), 500


@api.route(
    "/api/federated/train",
    methods=["POST"]
)
def federated_train():

    return start_federated_training()


# ============================================================
# ALTERNATIVE FEDERATED TRAINING ENDPOINT
# ============================================================

@api.route(
    "/api/federated-training",
    methods=["POST"]
)
def federated_training():

    return start_federated_training()