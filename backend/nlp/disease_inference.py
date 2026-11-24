import re


# ============================================================
# DISEASE INFERENCE FROM NLP FINDINGS
# ============================================================

def infer_possible_diseases(report, nlp_result):
    """
    Infer possible disease indicators from symptoms,
    conditions and measurements extracted from a medical report.

    This is a screening / educational inference layer.
    It is NOT a medical diagnosis.
    """

    report_text = str(report).lower()

    symptoms = [
        str(item).lower()
        for item in nlp_result.get("symptoms", [])
    ]

    conditions = [
        str(item).lower()
        for item in nlp_result.get("conditions", [])
    ]

    measurements = nlp_result.get("measurements", {})

    # Convert everything into one searchable text
    evidence_text = " ".join(
        symptoms + conditions + [report_text]
    )

    predictions = []

    # ========================================================
    # DIABETES
    # ========================================================

    diabetes_score = 0
    diabetes_evidence = []

    diabetes_symptoms = {
        "frequent urination": 2,
        "polyuria": 2,
        "urination": 1,
        "thirst": 2,
        "increased thirst": 2,
        "excessive thirst": 2,
        "polydipsia": 2,
        "fatigue": 1,
        "tired": 1,
        "weakness": 1,
        "weight loss": 2,
        "sudden weight loss": 2,
        "blurred vision": 1,
        "increased hunger": 1,
        "excessive hunger": 1,
    }

    for symptom, weight in diabetes_symptoms.items():
        if symptom in evidence_text:
            diabetes_score += weight
            diabetes_evidence.append(symptom)

    # Glucose measurement
    glucose_value = extract_measurement(
        measurements,
        ["glucose", "blood glucose", "blood sugar"]
    )

    if glucose_value is not None:

        if glucose_value >= 126:
            diabetes_score += 4
            diabetes_evidence.append(
                f"glucose value {glucose_value}"
            )

        elif glucose_value >= 100:
            diabetes_score += 2
            diabetes_evidence.append(
                f"glucose value {glucose_value}"
            )

    if diabetes_score >= 4:

        predictions.append({
            "disease": "Diabetes",
            "level": "Possible",
            "score": diabetes_score,
            "evidence": unique_list(
                diabetes_evidence
            ),
            "message":
                "The report contains symptoms or glucose "
                "findings that may be associated with diabetes."
        })

    # ========================================================
    # HYPERTENSION
    # ========================================================

    hypertension_score = 0
    hypertension_evidence = []

    bp = extract_blood_pressure(
        report_text,
        measurements
    )

    if bp is not None:

        systolic, diastolic = bp

        if systolic >= 180 or diastolic >= 120:
            hypertension_score += 5

        elif systolic >= 140 or diastolic >= 90:
            hypertension_score += 4

        elif systolic >= 130 or diastolic >= 80:
            hypertension_score += 2

        hypertension_evidence.append(
            f"blood pressure {systolic}/{diastolic}"
        )

    hypertension_terms = [
        "high blood pressure",
        "hypertension",
        "elevated blood pressure",
    ]

    for term in hypertension_terms:

        if term in evidence_text:
            hypertension_score += 4
            hypertension_evidence.append(term)

    if hypertension_score >= 3:

        predictions.append({
            "disease": "Hypertension",
            "level": "Possible",
            "score": hypertension_score,
            "evidence": unique_list(
                hypertension_evidence
            ),
            "message":
                "The report contains blood-pressure findings "
                "that may be associated with hypertension."
        })

    # ========================================================
    # HEART DISEASE
    # ========================================================

    heart_score = 0
    heart_evidence = []

    heart_terms = {
        "chest pain": 3,
        "chest discomfort": 3,
        "shortness of breath": 2,
        "breathlessness": 2,
        "palpitations": 2,
        "irregular heartbeat": 2,
        "dizziness": 1,
        "fainting": 2,
        "heart disease": 4,
        "coronary disease": 4,
    }

    for term, weight in heart_terms.items():

        if term in evidence_text:
            heart_score += weight
            heart_evidence.append(term)

    if heart_score >= 4:

        predictions.append({
            "disease": "Heart Disease",
            "level": "Possible",
            "score": heart_score,
            "evidence": unique_list(
                heart_evidence
            ),
            "message":
                "The report contains symptoms or findings "
                "that may require cardiovascular evaluation."
        })

    # ========================================================
    # KIDNEY DISEASE
    # ========================================================

    kidney_score = 0
    kidney_evidence = []

    kidney_terms = {
        "kidney disease": 5,
        "chronic kidney disease": 5,
        "kidney failure": 5,
        "swelling": 1,
        "edema": 2,
        "foamy urine": 3,
        "blood in urine": 3,
        "reduced urine": 2,
    }

    for term, weight in kidney_terms.items():

        if term in evidence_text:
            kidney_score += weight
            kidney_evidence.append(term)

    creatinine = extract_measurement(
        measurements,
        ["creatinine", "serum creatinine"]
    )

    if creatinine is not None:

        if creatinine > 1.3:
            kidney_score += 4
            kidney_evidence.append(
                f"creatinine value {creatinine}"
            )

    blood_urea = extract_measurement(
        measurements,
        ["blood urea", "urea", "bun"]
    )

    if blood_urea is not None:

        if blood_urea > 40:
            kidney_score += 3
            kidney_evidence.append(
                f"urea/BUN value {blood_urea}"
            )

    if kidney_score >= 4:

        predictions.append({
            "disease": "Kidney Disease",
            "level": "Possible",
            "score": kidney_score,
            "evidence": unique_list(
                kidney_evidence
            ),
            "message":
                "The report contains findings that may be "
                "associated with kidney problems."
        })

    # ========================================================
    # LIVER DISEASE
    # ========================================================

    liver_score = 0
    liver_evidence = []

    liver_terms = {
        "liver disease": 5,
        "hepatitis": 5,
        "jaundice": 4,
        "yellow eyes": 4,
        "yellow skin": 4,
        "abdominal pain": 1,
        "loss of appetite": 1,
    }

    for term, weight in liver_terms.items():

        if term in evidence_text:
            liver_score += weight
            liver_evidence.append(term)

    bilirubin = extract_measurement(
        measurements,
        ["bilirubin", "total bilirubin"]
    )

    if bilirubin is not None:

        if bilirubin > 1.2:
            liver_score += 3
            liver_evidence.append(
                f"bilirubin value {bilirubin}"
            )

    alt = extract_measurement(
        measurements,
        ["alt", "sgpt"]
    )

    if alt is not None:

        if alt > 40:
            liver_score += 3
            liver_evidence.append(
                f"ALT/SGPT value {alt}"
            )

    ast = extract_measurement(
        measurements,
        ["ast", "sgot"]
    )

    if ast is not None:

        if ast > 40:
            liver_score += 3
            liver_evidence.append(
                f"AST/SGOT value {ast}"
            )

    if liver_score >= 4:

        predictions.append({
            "disease": "Liver Disease",
            "level": "Possible",
            "score": liver_score,
            "evidence": unique_list(
                liver_evidence
            ),
            "message":
                "The report contains findings that may be "
                "associated with liver problems."
        })

    # ========================================================
    # TUBERCULOSIS
    # ========================================================

    tb_score = 0
    tb_evidence = []

    tb_terms = {
        "persistent cough": 3,
        "chronic cough": 3,
        "cough": 1,
        "coughing blood": 4,
        "blood in sputum": 4,
        "night sweats": 3,
        "fever": 2,
        "weight loss": 2,
        "loss of weight": 2,
        "tuberculosis": 5,
        "tb": 5,
    }

    for term, weight in tb_terms.items():

        if term in evidence_text:
            tb_score += weight
            tb_evidence.append(term)

    if tb_score >= 4:

        predictions.append({
            "disease": "Tuberculosis",
            "level": "Possible",
            "score": tb_score,
            "evidence": unique_list(
                tb_evidence
            ),
            "message":
                "The report contains symptoms that can occur "
                "with tuberculosis and may require further testing."
        })

    # ========================================================
    # SORT BY SCORE
    # ========================================================

    predictions.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return predictions


# ============================================================
# HELPERS
# ============================================================

def unique_list(items):

    result = []

    for item in items:

        if item not in result:
            result.append(item)

    return result


def extract_measurement(measurements, names):

    if not isinstance(measurements, dict):
        return None

    # Exact / direct match
    for name in names:

        if name in measurements:

            value = measurements[name]

            try:
                return float(value)

            except (ValueError, TypeError):
                pass

    # Case-insensitive search
    for key, value in measurements.items():

        key_lower = str(key).lower()

        for name in names:

            if name.lower() in key_lower:

                try:
                    return float(value)

                except (ValueError, TypeError):
                    pass

    return None


def extract_blood_pressure(
    report_text,
    measurements
):

    # Examples:
    # BP 150/95
    # Blood pressure: 150/95
    # blood pressure is 150/95

    patterns = [
        r"(?:blood pressure|bp)\s*(?:is|:)?\s*(\d{2,3})\s*/\s*(\d{2,3})",
        r"\b(\d{2,3})\s*/\s*(\d{2,3})\s*mmhg\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            report_text,
            re.IGNORECASE
        )

        if match:

            return (
                int(match.group(1)),
                int(match.group(2))
            )

    # Check extracted measurements
    if isinstance(measurements, dict):

        systolic = None
        diastolic = None

        for key, value in measurements.items():

            key_lower = str(key).lower()

            if "systolic" in key_lower:

                try:
                    systolic = float(value)

                except (ValueError, TypeError):
                    pass

            if "diastolic" in key_lower:

                try:
                    diastolic = float(value)

                except (ValueError, TypeError):
                    pass

        if systolic is not None and diastolic is not None:

            return (
                systolic,
                diastolic
            )

    return None