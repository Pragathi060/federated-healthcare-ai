# Disease configuration for the
# Adaptive Privacy-Preserving Federated Deep Learning Framework

DISEASE_CONFIG = {

    "diabetes": {
        "name": "Diabetes",
        "type": "tabular",
        "model_type": "MLP",
        "target": "class",
        "model_file": "diabetes_model.pth",
        "features": [
            "age",
            "gender",
            "polyuria",
            "polydipsia",
            "sudden_weight_loss",
            "weakness",
            "polyphagia",
            "genital_thrush",
            "visual_blurring",
            "itching",
            "irritability",
            "delayed_healing",
            "partial_paresis",
            "muscle_stiffness",
            "alopecia",
            "obesity"
        ]
    },

    "hypertension": {
        "name": "Hypertension",
        "type": "tabular",
        "model_type": "MLP",
        "target": "level",
        "model_file": "hypertension_model.pth",
        "features": [
            "age",
            "sex",
            "BMI",
            "Resi",
            "SBP",
            "DBP",
            "Smoking",
            "odisease",
            "creantine",
            "BUN",
            "Noofmed"
        ]
    },

    "heart": {
        "name": "Heart Disease",
        "type": "tabular",
        "model_type": "MLP",
        "target": "Outcome",
        "model_file": "heart_model.pth",
        "features": [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal"
        ]
    },

    "kidney": {
        "name": "Kidney Disease",
        "type": "tabular",
        "model_type": "MLP",
        "target": "class",
        "model_file": "kidney_model.pth",
        "features": [
            "age",
            "bp",
            "sg",
            "al",
            "su",
            "bgr",
            "bu",
            "sc",
            "sod",
            "pot",
            "hemo",
            "pcv",
            "wbcc",
            "rbcc"
        ]
    },

    "liver": {
        "name": "Liver Disease",
        "type": "tabular",
        "model_type": "MLP",
        "target": "Selector",
        "model_file": "liver_model.pth",
        "features": [
            "Age",
            "Gender",
            "TB",
            "DB",
            "Alkphos",
            "Sgpt",
            "Sgot",
            "TP",
            "ALB",
            "A/G Ratio"
        ]
    },

    "tuberculosis": {
        "name": "Tuberculosis",
        "type": "image",
        "model_type": "CNN",
        "target": "class",
        "model_file": "tb_model.pth",
        "federated_model_file": "tb_federated_model.pth",
        "features": []
    }
}


def get_disease_config(disease):
    """
    Return configuration for a selected disease.
    """

    disease = disease.lower()

    if disease not in DISEASE_CONFIG:
        raise ValueError(
            f"Unsupported disease: {disease}"
        )

    return DISEASE_CONFIG[disease]


def get_supported_diseases():
    """
    Return all supported diseases.
    """

    return list(DISEASE_CONFIG.keys())