import React, { useEffect, useState } from "react";
import "../styles/Prediction.css";

/* =========================================================
   DISEASE INPUT CONFIGURATION
   ========================================================= */

const diseaseFields = {
  /* =========================
     DIABETES
     ========================= */

  diabetes: [
    {
      key: "age",
      label: "Age",
      type: "number",
      placeholder: "Enter age",
      min: 1,
      max: 120,
    },
    {
      key: "gender",
      label: "Gender",
      type: "select",
      options: [
        ["Male", "Male"],
        ["Female", "Female"],
      ],
    },
    {
      key: "polyuria",
      label: "Do you urinate very often?",
      type: "yesno",
    },
    {
      key: "polydipsia",
      label: "Do you feel unusually thirsty often?",
      type: "yesno",
    },
    {
      key: "sudden_weight_loss",
      label: "Have you experienced sudden weight loss?",
      type: "yesno",
    },
    {
      key: "weakness",
      label: "Do you often feel weak or tired?",
      type: "yesno",
    },
    {
      key: "polyphagia",
      label: "Do you feel unusually hungry often?",
      type: "yesno",
    },
    {
      key: "genital_thrush",
      label: "Have you had repeated fungal infections?",
      type: "yesno",
    },
    {
      key: "visual_blurring",
      label: "Do you experience blurred vision?",
      type: "yesno",
    },
    {
      key: "itching",
      label: "Do you often experience itching?",
      type: "yesno",
    },
    {
      key: "irritability",
      label: "Do you often feel unusually irritated?",
      type: "yesno",
    },
    {
      key: "delayed_healing",
      label: "Do cuts or wounds take a long time to heal?",
      type: "yesno",
    },
    {
      key: "partial_paresis",
      label: "Do you experience weakness or difficulty moving?",
      type: "yesno",
    },
    {
      key: "muscle_stiffness",
      label: "Do you often experience muscle stiffness?",
      type: "yesno",
    },
    {
      key: "alopecia",
      label: "Are you experiencing unusual hair loss?",
      type: "yesno",
    },
    {
      key: "obesity",
      label: "Are you overweight?",
      type: "yesno",
    },
  ],

  /* =========================
     HYPERTENSION
     ========================= */

  hypertension: [
    {
      key: "age",
      label: "Age Group",
      type: "select",
      options: [
        ["0", "Below 35 years"],
        ["1", "35–55 years"],
        ["2", "Above 55 years"],
      ],
    },
    {
      key: "sex",
      label: "Gender",
      type: "select",
      options: [
        ["0", "Female"],
        ["1", "Male"],
      ],
    },
    {
      key: "BMI",
      label: "BMI Category",
      type: "select",
      options: [
        ["0", "Underweight"],
        ["1", "Healthy weight"],
        ["2", "Overweight / Obese"],
      ],
    },
    {
      key: "Resi",
      label: "Place of Residence",
      type: "select",
      options: [
        ["0", "Rural"],
        ["1", "Urban"],
      ],
    },
    {
      key: "SBP",
      label: "Systolic Blood Pressure",
      type: "select",
      options: [
        ["0", "Below 130 mmHg"],
        ["1", "130–179 mmHg"],
        ["2", "180 mmHg or above"],
      ],
    },
    {
      key: "DBP",
      label: "Diastolic Blood Pressure",
      type: "select",
      options: [
        ["0", "Below 80 mmHg"],
        ["1", "80–119 mmHg"],
        ["2", "120 mmHg or above"],
      ],
    },
    {
      key: "Smoking",
      label: "Do you smoke?",
      type: "yesno",
    },
    {
      key: "odisease",
      label: "Other Health Condition",
      type: "select",
      options: [
        ["0", "None"],
        ["1", "Diabetes"],
        ["2", "Kidney Disease"],
        ["3", "Other Disease"],
      ],
    },
    {
      key: "creantine",
      label: "Creatinine Level",
      type: "select",
      options: [
        ["0", "1 or below"],
        ["1", "Above 1"],
      ],
    },
    {
      key: "BUN",
      label: "Blood Urea Nitrogen (BUN)",
      type: "select",
      options: [
        ["0", "35 or below"],
        ["1", "Above 35"],
      ],
    },
    {
      key: "Noofmed",
      label: "Blood Pressure Medicines",
      type: "select",
      options: [
        ["0", "Not taking any medicine"],
        ["1", "One medicine"],
        ["2", "Two or more medicines"],
      ],
    },
  ],

  /* =========================
     HEART DISEASE
     ========================= */

  heart: [
    {
      key: "age",
      label: "Age",
      type: "number",
      placeholder: "Enter age",
      min: 1,
      max: 120,
    },
    {
      key: "sex",
      label: "Gender",
      type: "select",
      options: [
        ["0", "Female"],
        ["1", "Male"],
      ],
    },
    {
      key: "cp",
      label: "Chest Pain Type",
      type: "select",
      options: [
        ["1", "Typical angina"],
        ["2", "Atypical angina"],
        ["3", "Non-anginal pain"],
        ["4", "No typical chest pain"],
      ],
    },
    {
      key: "trestbps",
      label: "Resting Blood Pressure (mmHg)",
      type: "number",
      placeholder: "Example: 120",
      min: 50,
      max: 250,
    },
    {
      key: "chol",
      label: "Cholesterol (mg/dL)",
      type: "number",
      placeholder: "Example: 200",
      min: 50,
      max: 700,
    },
    {
      key: "fbs",
      label: "Fasting Blood Sugar",
      type: "select",
      options: [
        ["0", "120 mg/dL or below"],
        ["1", "Above 120 mg/dL"],
      ],
    },
    {
      key: "restecg",
      label: "Resting ECG Result",
      type: "select",
      options: [
        ["0", "Normal"],
        ["1", "ST-T wave abnormality"],
        ["2", "Left ventricular hypertrophy"],
      ],
    },
    {
      key: "thalach",
      label: "Maximum Heart Rate",
      type: "number",
      placeholder: "Example: 150",
      min: 50,
      max: 250,
    },
    {
      key: "exang",
      label: "Chest pain during exercise?",
      type: "yesno",
    },
    {
      key: "oldpeak",
      label: "ST Depression",
      type: "number",
      placeholder: "Enter value from ECG report",
      step: "0.1",
      min: 0,
      max: 10,
    },
    {
      key: "slope",
      label: "ST Segment Slope",
      type: "select",
      options: [
        ["1", "Upsloping"],
        ["2", "Flat"],
        ["3", "Downsloping"],
      ],
    },
    {
      key: "ca",
      label: "Number of Major Blood Vessels",
      type: "select",
      options: [
        ["0", "0"],
        ["1", "1"],
        ["2", "2"],
        ["3", "3"],
      ],
    },
    {
      key: "thal",
      label: "Thalassemia Test Result",
      type: "select",
      options: [
        ["3", "Normal"],
        ["6", "Fixed defect"],
        ["7", "Reversible defect"],
      ],
    },
  ],

  /* =========================
     KIDNEY DISEASE
     ========================= */

  kidney: [
    {
      key: "age",
      label: "Age",
      type: "number",
      placeholder: "Enter age",
      min: 1,
      max: 120,
    },
    {
      key: "bp",
      label: "Blood Pressure (mmHg)",
      type: "number",
      placeholder: "Example: 80",
    },
    {
      key: "sg",
      label: "Urine Specific Gravity",
      type: "select",
      options: [
        ["1.005", "1.005"],
        ["1.010", "1.010"],
        ["1.015", "1.015"],
        ["1.020", "1.020"],
        ["1.025", "1.025"],
      ],
    },
    {
      key: "al",
      label: "Urine Albumin Level",
      type: "select",
      options: [
        ["0", "0 - Normal"],
        ["1", "1"],
        ["2", "2"],
        ["3", "3"],
        ["4", "4"],
        ["5", "5"],
      ],
    },
    {
      key: "su",
      label: "Urine Sugar Level",
      type: "select",
      options: [
        ["0", "0 - Normal"],
        ["1", "1"],
        ["2", "2"],
        ["3", "3"],
        ["4", "4"],
        ["5", "5"],
      ],
    },
    {
      key: "bgr",
      label: "Blood Glucose (mg/dL)",
      type: "number",
      placeholder: "From laboratory report",
    },
    {
      key: "bu",
      label: "Blood Urea (mg/dL)",
      type: "number",
      placeholder: "From laboratory report",
    },
    {
      key: "sc",
      label: "Serum Creatinine (mg/dL)",
      type: "number",
      step: "0.1",
      placeholder: "Example: 1.2",
    },
    {
      key: "sod",
      label: "Sodium (mEq/L)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "pot",
      label: "Potassium (mEq/L)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "hemo",
      label: "Hemoglobin (g/dL)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "pcv",
      label: "Packed Cell Volume (%)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "wbcc",
      label: "White Blood Cell Count",
      type: "number",
      placeholder: "From laboratory report",
    },
    {
      key: "rbcc",
      label: "Red Blood Cell Count",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
  ],

  /* =========================
     LIVER DISEASE
     ========================= */

  liver: [
    {
      key: "Age",
      label: "Age",
      type: "number",
      placeholder: "Enter age",
      min: 1,
      max: 120,
    },
    {
      key: "Gender",
      label: "Gender",
      type: "select",
      options: [
        ["Male", "Male"],
        ["Female", "Female"],
      ],
    },
    {
      key: "TB",
      label: "Total Bilirubin (mg/dL)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "DB",
      label: "Direct Bilirubin (mg/dL)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "Alkphos",
      label: "Alkaline Phosphatase (IU/L)",
      type: "number",
      placeholder: "From laboratory report",
    },
    {
      key: "Sgpt",
      label: "ALT / SGPT (IU/L)",
      type: "number",
      placeholder: "From laboratory report",
    },
    {
      key: "Sgot",
      label: "AST / SGOT (IU/L)",
      type: "number",
      placeholder: "From laboratory report",
    },
    {
      key: "TP",
      label: "Total Protein (g/dL)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "ALB",
      label: "Albumin (g/dL)",
      type: "number",
      step: "0.1",
      placeholder: "From laboratory report",
    },
    {
      key: "A/G Ratio",
      label: "Albumin / Globulin Ratio",
      type: "number",
      step: "0.01",
      placeholder: "From laboratory report",
    },
  ],
};

/* =========================================================
   DISEASE NAMES
   ========================================================= */

const diseaseNames = {
  diabetes: "Diabetes",
  hypertension: "Hypertension",
  heart: "Heart Disease",
  kidney: "Kidney Disease",
  liver: "Liver Disease",
  tuberculosis: "Tuberculosis",
};

/* =========================================================
   COMPONENT
   ========================================================= */

export default function Prediction({ api, health }) {
  const [disease, setDisease] = useState("diabetes");
  const [form, setForm] = useState({});
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (health === "Backend connected") {
      setError("");
    }
  }, [health]);
  /* =========================================================
     CHANGE DISEASE
     ========================================================= */

  const changeDisease = (event) => {
    setDisease(event.target.value);
    setForm({});
    setImage(null);
    setResult(null);
    setError("");
  };

  /* =========================================================
     HANDLE INPUT
     ========================================================= */

  const handleChange = (key, value) => {
    setForm((previous) => ({
      ...previous,
      [key]: value,
    }));

    setResult(null);
    setError("");
  };

  /* =========================================================
     PATIENT-FRIENDLY RESULT
     ========================================================= */

  const getPatientPrediction = () => {
    if (!result) {
      return "";
    }

    if (result.disease === "Diabetes") {
      return result.prediction === 0
        ? "No Diabetes Risk Detected"
        : "Possible Diabetes Risk";
    }

    if (result.disease === "Hypertension") {
      if (result.prediction === 0) {
        return "Lower Blood Pressure Risk";
      }

      if (result.prediction === 1) {
        return "Moderate Blood Pressure Risk";
      }

      return "Higher Blood Pressure Risk";
    }

    if (result.disease === "Heart Disease") {
      return result.prediction === 0
        ? "No Heart Disease Risk Detected"
        : "Possible Heart Disease Risk";
    }

    if (result.disease === "Kidney Disease") {
      return result.prediction === 0
        ? "No Kidney Disease Risk Detected"
        : "Possible Kidney Disease Risk";
    }

    if (result.disease === "Liver Disease") {
      return result.prediction === 0
        ? "No Liver Disease Risk Detected"
        : "Possible Liver Disease Risk";
    }

    if (result.disease === "Tuberculosis") {
      return result.prediction === 0
        ? "Normal Chest X-ray"
        : "Possible Tuberculosis";
    }

    return result.prediction_label || "Prediction completed";
  };

  /* =========================================================
     RISK LEVEL
     ========================================================= */

  const getRiskLevel = () => {
    if (!result) {
      return "";
    }

    if (result.disease === "Hypertension") {
      if (result.prediction === 0) {
        return "Low";
      }

      if (result.prediction === 1) {
        return "Moderate";
      }

      return "High";
    }

    return result.prediction === 0 ? "Low" : "Higher";
  };

  /* =========================================================
     CONFIDENCE
     ========================================================= */

  const getConfidence = () => {
    if (!result) {
      return null;
    }

    if (typeof result.percentage === "number") {
      return result.percentage;
    }

    if (typeof result.probability === "number") {
      return result.probability * 100;
    }

    return null;
  };

  /* =========================================================
     MODEL NAME
     ========================================================= */

  const getModelName = () => {
    if (!result) {
      return "Federated Deep Learning";
    }

    if (result.model === "CNN") {
      return "Federated Deep Learning CNN";
    }

    if (result.model) {
      return `Federated Deep Learning ${result.model}`;
    }

    return "Federated Deep Learning MLP";
  };

  /* =========================================================
     PREDICTION
     ========================================================= */

  const predict = async (event) => {
    event.preventDefault();

    setResult(null);
    setError("");
    setLoading(true);

    try {
      let response;

      /* =========================
         TB PREDICTION
         ========================= */

      if (disease === "tuberculosis") {
        if (!image) {
          setError("Please upload a chest X-ray image.");
          setLoading(false);
          return;
        }

        const formData = new FormData();
        formData.append("image", image);

        response = await fetch(`${api}/predict/tuberculosis`, {
          method: "POST",
          body: formData,
        });
      }

      /* =========================
         TABULAR PREDICTION
         ========================= */

      else {
        const requestData = {
          disease: disease,
          ...form,
        };

        response = await fetch(`${api}/predict`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });
      }

      const data = await response.json();

      if (!response.ok) {
        setError(
          data.message ||
            data.error ||
            "Prediction failed. Please check the entered information."
        );
        return;
      }

      setResult(data);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to the backend. Please make sure the backend server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =========================================================
     RESET
     ========================================================= */

  const resetForm = () => {
    setForm({});
    setImage(null);
    setResult(null);
    setError("");
  };

  /* =========================================================
     RENDER
     ========================================================= */

  return (
    <section className="prediction-page">

      {/* =========================
          PAGE HEADER
          ========================= */}

      <div className="prediction-header">
        <h3>Disease Prediction</h3>

        <p>
          Enter the patient's health information to get an
          AI-based disease risk prediction.
        </p>
      </div>

      {/* =========================
          DISEASE SELECTOR
          ========================= */}

      <div className="disease-selector-card">
        <label>
          Select Disease

          <select
            value={disease}
            onChange={changeDisease}
          >
            <option value="diabetes">
              Diabetes
            </option>

            <option value="hypertension">
              Hypertension
            </option>

            <option value="heart">
              Heart Disease
            </option>

            <option value="kidney">
              Kidney Disease
            </option>

            <option value="liver">
              Liver Disease
            </option>

            <option value="tuberculosis">
              Tuberculosis
            </option>
          </select>
        </label>
      </div>

      {/* =========================
          TB FORM
          ========================= */}

      {disease === "tuberculosis" ? (

        <form
          className="prediction-form-card"
          onSubmit={predict}
        >

          <div className="xray-upload">

            <h4>Chest X-ray Analysis</h4>

            <p>
              Upload a chest X-ray image for AI-based
              tuberculosis risk analysis.
            </p>

            <input
              type="file"
              accept="image/*"
              onChange={(event) => {
                const selectedImage =
                  event.target.files[0];

                setImage(selectedImage || null);
                setResult(null);
                setError("");
              }}
              required
            />

            {image && (
              <div className="xray-preview">

                <p>
                  Selected image:{" "}
                  <strong>{image.name}</strong>
                </p>

                <img
                  src={URL.createObjectURL(image)}
                  alt="Selected chest X-ray"
                />

              </div>
            )}

          </div>

          <div className="prediction-actions">

            <button
              type="submit"
              className="predict-button"
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Analyze Chest X-ray"}
            </button>

            <button
              type="button"
              className="reset-button"
              onClick={resetForm}
              disabled={loading}
            >
              Reset
            </button>

          </div>

        </form>

      ) : (

        /* =========================
           TABULAR FORM
           ========================= */

        <form
          className="prediction-form-card"
          onSubmit={predict}
        >

          <div className="prediction-form-grid">

            {diseaseFields[disease].map((field) => {

              const {
                key,
                label,
                type,
                options,
                placeholder,
                min,
                max,
                step,
              } = field;

              return (
                <div
                  className="prediction-field"
                  key={key}
                >

                  <label>
                    {label}
                  </label>

                  {/* NUMBER INPUT */}

                  {type === "number" && (
                    <input
                      type="number"
                      step={step || "any"}
                      min={min}
                      max={max}
                      placeholder={placeholder}
                      value={form[key] ?? ""}
                      onChange={(event) =>
                        handleChange(
                          key,
                          event.target.value
                        )
                      }
                      required
                    />
                  )}

                  {/* YES / NO */}

                  {type === "yesno" && (
                    <select
                      value={form[key] ?? ""}
                      onChange={(event) =>
                        handleChange(
                          key,
                          event.target.value
                        )
                      }
                      required
                    >
                      <option value="">
                        Select
                      </option>

                      <option value="Yes">
                        Yes
                      </option>

                      <option value="No">
                        No
                      </option>
                    </select>
                  )}

                  {/* DROPDOWN */}

                  {type === "select" && (
                    <select
                      value={form[key] ?? ""}
                      onChange={(event) =>
                        handleChange(
                          key,
                          event.target.value
                        )
                      }
                      required
                    >
                      <option value="">
                        Select
                      </option>

                      {options.map(
                        ([value, text]) => (
                          <option
                            key={value}
                            value={value}
                          >
                            {text}
                          </option>
                        )
                      )}
                    </select>
                  )}

                </div>
              );
            })}

            {/* =========================
                MEDICATION INFORMATION
                ========================= */}

            {disease === "hypertension" && (
              <div className="medication-info">

                <div className="medication-icon">
                  💊
                </div>

                <div className="medication-info-content">

                  <p className="medication-info-title">
                    Medication Information
                  </p>

                  <p className="medication-info-text">
                    Medication use is optional.
                    Select "Not taking any medicine"
                    if the patient is not currently
                    taking blood pressure medicine.
                  </p>

                </div>

              </div>
            )}

            {/* =========================
                ACTION BUTTONS
                ========================= */}

            <div className="prediction-actions">

              <button
                type="submit"
                className="predict-button"
                disabled={loading}
              >
                {loading
                  ? "Analyzing..."
                  : `Check ${diseaseNames[disease]}`}
              </button>

              <button
                type="button"
                className="reset-button"
                onClick={resetForm}
                disabled={loading}
              >
                Reset
              </button>

            </div>

          </div>

        </form>
      )}

      {/* =========================
          ERROR
          ========================= */}

      {error && health !== "Backend connected" && (
        <div className="prediction-error">
          {error}
        </div>
      )}

      {/* =========================
          RESULT
          ========================= */}

      {result &&
        result.status === "success" && (

          <div className="prediction-result">

            {/* RESULT HEADER */}

            <div className="prediction-result-header">

              <h3>
                Prediction Result
              </h3>

              <p>
                AI analysis completed successfully.
              </p>

            </div>

            {/* MAIN RESULT */}

            <div className="prediction-main">

              <div className="prediction-highlight">

                <div className="prediction-highlight-label">
                  Disease
                </div>

                <div className="prediction-disease">
                  {result.disease}
                </div>

                <div className="prediction-highlight-label">
                  AI Prediction
                </div>

                <div className="prediction-text">
                  {getPatientPrediction()}
                </div>

              </div>

              {/* RISK */}

              <div className="risk-card">

                <div className="risk-label">
                  Risk Level
                </div>

                <div className="risk-value">
                  {getRiskLevel()}
                </div>

              </div>

            </div>

            {/* =========================
                MODEL DETAILS
                ========================= */}

            <div className="model-details">

              <div className="model-detail">

                <span className="model-detail-label">
                  AI Model
                </span>

                <span className="model-detail-value">
                  {getModelName()}
                </span>

              </div>

              <div className="model-detail">

                <span className="model-detail-label">
                  Prediction Type
                </span>

                <span className="model-detail-value">
                  Disease Risk Prediction
                </span>

              </div>

            </div>

            {/* =========================
                CONFIDENCE
                ========================= */}

           {getConfidence() !== null && (
  <div className="confidence-section">

    <div className="confidence-header">

      <span className="confidence-title">
        Prediction Score
      </span>

      <span className="confidence-value">
        {getConfidence().toFixed(1)}%
      </span>
                </div>

                <div className="confidence-bar">

                  <div
                    className="confidence-fill"
                    style={{
                      width: `${Math.min(
                        Math.max(
                          getConfidence(),
                          0
                        ),
                        100
                      )}%`,
                    }}
                  />

                </div>

                <p className="confidence-note">
  Prediction score represents the model
  output and should not be interpreted
  as clinical certainty.
</p>

              </div>
            )}

            {/* =========================
                PRIVACY
                ========================= */}

            <div className="privacy-card">

              <h4>
                🔒 Privacy-Preserving AI
              </h4>

              <p>
                The system is designed around
                federated learning, where participating
                hospital nodes train models locally and
                share model parameters rather than raw
                patient records.
              </p>

            </div>

            {/* =========================
                DISCLAIMER
                ========================= */}

            <div className="prediction-disclaimer">

              <h4>
                Important Notice
              </h4>

              <p>
                This result is generated by an AI
                research prototype for educational
                purposes. It is not a confirmed medical
                diagnosis and must not be used as a
                substitute for professional medical
                evaluation.
              </p>

            </div>

            {/* =========================
                NEW PREDICTION
                ========================= */}

            <div className="new-prediction-wrapper">

              <button
                type="button"
                className="new-prediction-button"
                onClick={resetForm}
              >
                New Prediction
              </button>

            </div>

          </div>
        )}

    </section>
  );
}