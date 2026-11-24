from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-small"

tokenizer = None
model = None


def load_llm():
    global tokenizer, model

    if tokenizer is None or model is None:

        print("Loading local LLM...")

        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_NAME,
            low_cpu_mem_usage=False
        )

        model = model.to("cpu")

        print("LLM loaded successfully.")

    return tokenizer, model


def generate_clinical_explanation(report, nlp_result):

    symptoms = nlp_result.get("symptoms", [])
    conditions = nlp_result.get("conditions", [])
    medications = nlp_result.get("medications", [])
    measurements = nlp_result.get("measurements", {})

    symptoms_text = ", ".join(symptoms) if symptoms else "none"
    conditions_text = ", ".join(conditions) if conditions else "none"
    medications_text = ", ".join(medications) if medications else "none"

    measurements_text = ", ".join(
        f"{key}: {value}"
        for key, value in measurements.items()
    ) if measurements else "none"

    patient_information = (
        f"Symptoms: {symptoms_text}. "
        f"Conditions: {conditions_text}. "
        f"Medications: {medications_text}. "
        f"Measurements: {measurements_text}."
    )

    prompt = f"""
You are a healthcare information assistant.

Read the patient information below and provide a useful educational explanation.

Your response must:

1. Identify possible health conditions that may be associated with
   the symptoms and measurements.
2. Explain briefly why the findings may be related to those conditions.
3. Mention important measurements when available.
4. Clearly state that this is not a confirmed diagnosis.
5. Recommend consultation with a qualified healthcare professional.
6. Use simple English.
7. Do not prescribe medicines.
8. Do not give treatment instructions.
9. Do not simply repeat the input.

Patient information:
{patient_information}

Write the explanation now:
"""

    tokenizer, model = load_llm()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )

    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=150,
        num_beams=4,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    # ---------------------------------------------------------
    # FALLBACK EXPLANATION
    # ---------------------------------------------------------
    # Small local models may sometimes produce weak responses.
    # This fallback gives a useful explanation based on the
    # extracted NLP findings.
    # ---------------------------------------------------------

    if len(response.split()) < 12:

        explanation_parts = []

        if symptoms:
            explanation_parts.append(
                f"The reported symptoms include {symptoms_text}."
            )

        if measurements:
            explanation_parts.append(
                f"Recorded measurements include {measurements_text}."
            )

        # Diabetes-related findings
        diabetes_symptoms = {
            "fatigue",
            "thirst",
            "frequent urination",
            "weight loss",
            "increased hunger",
            "blurred vision"
        }

        found_diabetes_symptoms = (
            set(symptoms).intersection(diabetes_symptoms)
        )

        glucose_value = None

        if "glucose" in measurements:
            try:
                glucose_value = float(measurements["glucose"])
            except (ValueError, TypeError):
                glucose_value = None

        if len(found_diabetes_symptoms) >= 2 or (
            glucose_value is not None and glucose_value >= 126
        ):
            explanation_parts.append(
                "The combination of these findings may be associated "
                "with diabetes or elevated blood glucose."
            )

        # Hypertension-related findings
        if "blood pressure" in measurements:

            bp_value = str(
                measurements["blood pressure"]
            )

            try:
                systolic = int(
                    bp_value.split("/")[0].strip()
                )
                diastolic = int(
                    bp_value.split("/")[1].strip()
                )

                if systolic >= 140 or diastolic >= 90:
                    explanation_parts.append(
                        "The recorded blood pressure is elevated "
                        "and may be associated with hypertension."
                    )

            except (ValueError, IndexError):
                pass

        # Heart-related findings
        heart_symptoms = {
            "chest pain",
            "shortness of breath",
            "dizziness"
        }

        found_heart_symptoms = (
            set(symptoms).intersection(heart_symptoms)
        )

        if len(found_heart_symptoms) >= 2:
            explanation_parts.append(
                "The combination of chest-related symptoms "
                "may warrant evaluation for a cardiovascular condition."
            )

        # Kidney-related findings
        kidney_symptoms = {
            "weakness",
            "nausea",
            "swelling"
        }

        found_kidney_symptoms = (
            set(symptoms).intersection(kidney_symptoms)
        )

        if len(found_kidney_symptoms) >= 2:
            explanation_parts.append(
                "These findings may also warrant evaluation "
                "of kidney function."
            )

        if not explanation_parts:
            explanation_parts.append(
                "The available information does not provide "
                "enough evidence to identify a specific possible "
                "health condition."
            )

        explanation_parts.append(
            "These findings do not confirm a medical diagnosis. "
            "A qualified healthcare professional should be consulted "
            "for proper medical evaluation."
        )

        response = " ".join(explanation_parts)

    return response