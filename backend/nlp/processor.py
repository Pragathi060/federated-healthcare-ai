import re


# --------------------------------------------------
# Extract symptoms from medical text
# --------------------------------------------------

def extract_symptoms(text):

    symptoms = [
        "fever",
        "cough",
        "fatigue",
        "thirst",
        "frequent urination",
        "headache",
        "nausea",
        "vomiting",
        "dizziness",
        "shortness of breath",
        "chest pain",
        "weakness",
        "blurred vision",
        "weight loss",
        "weight gain"
    ]

    text_lower = text.lower()

    found_symptoms = []

    for symptom in symptoms:

        if symptom in text_lower:
            found_symptoms.append(symptom)

    return found_symptoms


# --------------------------------------------------
# Extract medical conditions
# --------------------------------------------------

def extract_conditions(text):

    conditions = [
        "diabetes",
        "hypertension",
        "asthma",
        "heart disease",
        "cardiovascular disease",
        "infection",
        "obesity",
        "kidney disease",
        "high blood pressure"
    ]

    text_lower = text.lower()

    found_conditions = []

    for condition in conditions:

        if condition in text_lower:
            found_conditions.append(condition)

    return found_conditions


# --------------------------------------------------
# Extract medications
# --------------------------------------------------

def extract_medications(text):

    medications = [
        "insulin",
        "metformin",
        "aspirin",
        "paracetamol",
        "ibuprofen",
        "atorvastatin",
        "amlodipine"
    ]

    text_lower = text.lower()

    found_medications = []

    for medication in medications:

        if medication in text_lower:
            found_medications.append(medication)

    return found_medications


# --------------------------------------------------
# Extract numerical medical measurements
# --------------------------------------------------

def extract_measurements(text):

    patterns = {

        "glucose":
            r"glucose\s*[:=]?\s*(\d+(?:\.\d+)?)",

        "blood pressure":
            r"blood pressure\s*[:=]?\s*(\d+\/\d+)",

        "bmi":
            r"bmi\s*[:=]?\s*(\d+(?:\.\d+)?)",

        "temperature":
            r"temperature\s*[:=]?\s*(\d+(?:\.\d+)?)",

        "heart rate":
            r"heart rate\s*[:=]?\s*(\d+(?:\.\d+)?)"
    }

    results = {}

    text_lower = text.lower()

    for name, pattern in patterns.items():

        match = re.search(
            pattern,
            text_lower
        )

        if match:
            results[name] = match.group(1)

    return results


# --------------------------------------------------
# Complete NLP analysis
# --------------------------------------------------

def analyze_report(text):

    return {

        "symptoms":
            extract_symptoms(text),

        "conditions":
            extract_conditions(text),

        "medications":
            extract_medications(text),

        "measurements":
            extract_measurements(text)
    }