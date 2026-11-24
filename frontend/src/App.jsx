import React, { useEffect, useState } from "react";

export default function Prediction({ api, health }) {
  const [disease, setDisease] = useState("diabetes");
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  /*
   * Clear stale backend error when the backend becomes available.
   */
  useEffect(() => {
    if (health === "Backend connected") {
      setError("");
    }
  }, [health]);

  const diseaseFields = {
    diabetes: [
      {
        name: "age",
        label: "Age",
        type: "number",
      },
      {
        name: "gender",
        label: "Gender",
        type: "number",
      },
      {
        name: "polyuria",
        label: "Polyuria",
        type: "number",
      },
      {
        name: "polydipsia",
        label: "Polydipsia",
        type: "number",
      },
      {
        name: "sudden_weight_loss",
        label: "Sudden Weight Loss",
        type: "number",
      },
      {
        name: "weakness",
        label: "Weakness",
        type: "number",
      },
      {
        name: "polyphagia",
        label: "Polyphagia",
        type: "number",
      },
      {
        name: "genital_thrush",
        label: "Genital Thrush",
        type: "number",
      },
      {
        name: "visual_blurring",
        label: "Visual Blurring",
        type: "number",
      },
      {
        name: "itching",
        label: "Itching",
        type: "number",
      },
      {
        name: "irritability",
        label: "Irritability",
        type: "number",
      },
      {
        name: "delayed_healing",
        label: "Delayed Healing",
        type: "number",
      },
      {
        name: "partial_paresis",
        label: "Partial Paresis",
        type: "number",
      },
      {
        name: "muscle_stiffness",
        label: "Muscle Stiffness",
        type: "number",
      },
      {
        name: "alopecia",
        label: "Alopecia",
        type: "number",
      },
      {
        name: "obesity",
        label: "Obesity",
        type: "number",
      },
    ],

    hypertension: [
      {
        name: "age",
        label: "Age",
        type: "number",
      },
      {
        name: "gender",
        label: "Gender",
        type: "number",
      },
      {
        name: "cp",
        label: "Chest Pain Type",
        type: "number",
      },
      {
        name: "trestbps",
        label: "Resting Blood Pressure",
        type: "number",
      },
      {
        name: "chol",
        label: "Cholesterol",
        type: "number",
      },
      {
        name: "fbs",
        label: "Fasting Blood Sugar",
        type: "number",
      },
      {
        name: "restecg",
        label: "Resting ECG",
        type: "number",
      },
      {
        name: "thalach",
        label: "Maximum Heart Rate",
        type: "number",
      },
      {
        name: "exang",
        label: "Exercise Induced Angina",
        type: "number",
      },
      {
        name: "oldpeak",
        label: "Oldpeak",
        type: "number",
      },
      {
        name: "noofmed",
        label: "Number of Medicines",
        type: "select",
        options: [
          {
            value: "0",
            label: "Not taking any medicine",
          },
          {
            value: "1",
            label: "One medicine",
          },
          {
            value: "2",
            label: "Two or more medicines",
          },
        ],
      },
    ],

    heart: [
      {
        name: "age",
        label: "Age",
        type: "number",
      },
      {
        name: "sex",
        label: "Sex",
        type: "number",
      },
      {
        name: "cp",
        label: "Chest Pain Type",
        type: "number",
      },
      {
        name: "trestbps",
        label: "Resting Blood Pressure",
        type: "number",
      },
      {
        name: "chol",
        label: "Cholesterol",
        type: "number",
      },
      {
        name: "fbs",
        label: "Fasting Blood Sugar",
        type: "number",
      },
      {
        name: "restecg",
        label: "Resting ECG",
        type: "number",
      },
      {
        name: "thalach",
        label: "Maximum Heart Rate",
        type: "number",
      },
      {
        name: "exang",
        label: "Exercise Induced Angina",
        type: "number",
      },
      {
        name: "oldpeak",
        label: "Oldpeak",
        type: "number",
      },
      {
        name: "slope",
        label: "Slope",
        type: "number",
      },
      {
        name: "ca",
        label: "Number of Major Vessels",
        type: "number",
      },
      {
        name: "thal",
        label: "Thalassemia",
        type: "number",
      },
    ],

    kidney: [
      {
        name: "age",
        label: "Age",
        type: "number",
      },
      {
        name: "blood_pressure",
        label: "Blood Pressure",
        type: "number",
      },
      {
        name: "specific_gravity",
        label: "Specific Gravity",
        type: "number",
      },
      {
        name: "albumin",
        label: "Albumin",
        type: "number",
      },
      {
        name: "sugar",
        label: "Sugar",
        type: "number",
      },
      {
        name: "blood_glucose_random",
        label: "Blood Glucose Random",
        type: "number",
      },
      {
        name: "blood_urea",
        label: "Blood Urea",
        type: "number",
      },
      {
        name: "serum_creatinine",
        label: "Serum Creatinine",
        type: "number",
      },
      {
        name: "sodium",
        label: "Sodium",
        type: "number",
      },
      {
        name: "potassium",
        label: "Potassium",
        type: "number",
      },
      {
        name: "hemoglobin",
        label: "Hemoglobin",
        type: "number",
      },
      {
        name: "packed_cell_volume",
        label: "Packed Cell Volume",
        type: "number",
      },
      {
        name: "white_blood_cell_count",
        label: "White Blood Cell Count",
        type: "number",
      },
      {
        name: "red_blood_cell_count",
        label: "Red Blood Cell Count",
        type: "number",
      },
    ],

    liver: [
      {
        name: "age",
        label: "Age",
        type: "number",
      },
      {
        name: "gender",
        label: "Gender",
        type: "number",
      },
      {
        name: "total_bilirubin",
        label: "Total Bilirubin",
        type: "number",
      },
      {
        name: "direct_bilirubin",
        label: "Direct Bilirubin",
        type: "number",
      },
      {
        name: "alkaline_phosphotase",
        label: "Alkaline Phosphotase",
        type: "number",
      },
      {
        name: "alamine_aminotransferase",
        label: "Alamine Aminotransferase",
        type: "number",
      },
      {
        name: "aspartate_aminotransferase",
        label: "Aspartate Aminotransferase",
        type: "number",
      },
      {
        name: "total_proteins",
        label: "Total Proteins",
        type: "number",
      },
      {
        name: "albumin",
        label: "Albumin",
        type: "number",
      },
      {
        name: "albumin_and_globulin_ratio",
        label: "Albumin and Globulin Ratio",
        type: "number",
      },
    ],
  };

  const diseaseNames = {
    diabetes: "Diabetes",
    hypertension: "Hypertension",
    heart: "Heart Disease",
    kidney: "Kidney Disease",
    liver: "Liver Disease",
    tuberculosis: "Tuberculosis",
  };

  const getFields = () => {
    if (disease === "tuberculosis") {
      return [];
    }

    return diseaseFields[disease] || [];
  };

  const handleDiseaseChange = (event) => {
    setDisease(event.target.value);
    setFormData({});
    setResult(null);
    setError("");
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

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

  const predict = async () => {
    setError("");
    setResult(null);

    if (health !== "Backend connected") {
      setError(
        "Backend is not connected. Please wait for the backend to become available."
      );
      return;
    }

    setLoading(true);

    try {
      const fields = getFields();

      const missingFields = fields.filter((field) => {
        return (
          formData[field.name] === undefined ||
          formData[field.name] === ""
        );
      });

      if (missingFields.length > 0) {
        setError("Please fill all the required fields.");
        setLoading(false);
        return;
      }

      const payload = {};

      fields.forEach((field) => {
        payload[field.name] = Number(formData[field.name]);
      });

      const response = await fetch(`${api}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          disease: disease,
          ...payload,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            data.message ||
            "Prediction request failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const confidence = getConfidence();

  return (
    <div className="prediction-page">

      <div className="page-title">
        <h2>Disease Risk Prediction</h2>

        <p>
          AI-based multi-disease risk prediction using
          federated deep learning.
        </p>
      </div>

      {/* BACKEND STATUS */}
      <div className="prediction-status-card">

        <div>
          <strong>Backend Status</strong>

          <p>
            {health}
          </p>
        </div>

        <div
          className={`prediction-status-dot ${
            health === "Backend connected"
              ? "online"
              : "offline"
          }`}
        >
          ●
        </div>

      </div>

      {/* DISEASE SELECTION */}
      <div className="prediction-card">

        <div className="card-header">
          <h3>Select Disease</h3>

          <p>
            Select the disease you want to evaluate.
          </p>
        </div>

        <select
          value={disease}
          onChange={handleDiseaseChange}
          className="disease-select"
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

      </div>

      {/* TB MESSAGE */}
      {disease === "tuberculosis" && (
        <div className="prediction-card">

          <div className="card-header">
            <h3>Tuberculosis Prediction</h3>

            <p>
              TB prediction uses a CNN model trained on
              chest X-ray images.
            </p>
          </div>

          <div className="tb-info">
            <p>
              Please use the tuberculosis image prediction
              section for uploading a chest X-ray.
            </p>
          </div>

        </div>
      )}

      {/* INPUT FORM */}
      {disease !== "tuberculosis" && (
        <div className="prediction-card">

          <div className="card-header">
            <h3>
              {diseaseNames[disease]} Information
            </h3>

            <p>
              Enter the required patient parameters.
            </p>
          </div>

          <div className="prediction-form">

            {getFields().map((field) => (
              <div
                className="form-group"
                key={field.name}
              >

                <label htmlFor={field.name}>
                  {field.label}
                </label>

                {field.type === "select" ? (
                  <select
                    id={field.name}
                    name={field.name}
                    value={formData[field.name] || ""}
                    onChange={handleChange}
                  >
                    <option value="">
                      Select an option
                    </option>

                    {field.options.map((option) => (
                      <option
                        key={option.value}
                        value={option.value}
                      >
                        {option.label}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    id={field.name}
                    name={field.name}
                    type={field.type}
                    value={formData[field.name] || ""}
                    onChange={handleChange}
                    placeholder={`Enter ${field.label}`}
                  />
                )}

              </div>
            ))}

          </div>

          {/* ERROR */}
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {/* PREDICT BUTTON */}
          <button
            className="predict-button"
            onClick={predict}
            disabled={
              loading ||
              health !== "Backend connected"
            }
          >
            {loading
              ? "Predicting..."
              : "Predict Disease Risk"}
          </button>

        </div>
      )}

      {/* RESULT */}
      {result && (
        <div className="prediction-result-card">

          <div className="result-header">
            <h3>
              Prediction Result
            </h3>

            <span className="result-success">
              Success
            </span>
          </div>

          <div className="result-main">

            <div className="result-disease">

              <span className="result-label">
                Disease
              </span>

              <strong>
                {result.disease ||
                  diseaseNames[disease]}
              </strong>

            </div>

            <div className="result-prediction">

              <span className="result-label">
                Prediction
              </span>

              <strong>
                {result.prediction_label ||
                  (result.prediction === 1
                    ? "High Risk"
                    : "Low Risk")}
              </strong>

            </div>

          </div>

          {/* PREDICTION SCORE */}
          {confidence !== null && (
            <div className="prediction-score">

              <div className="score-header">

                <span>
                  Prediction Score
                </span>

                <strong>
                  {confidence.toFixed(2)}%
                </strong>

              </div>

              <div className="score-bar">

                <div
                  className="score-fill"
                  style={{
                    width: `${Math.min(
                      Math.max(confidence, 0),
                      100
                    )}%`,
                  }}
                />

              </div>

              <p>
                This score represents the model's
                prediction probability and should not
                be interpreted as clinical certainty.
              </p>

            </div>
          )}

          {/* MODEL INFORMATION */}
          <div className="result-details">

            <div>
              <span>
                Model
              </span>

              <strong>
                {result.model || "Deep Learning"}
              </strong>
            </div>

            <div>
              <span>
                Learning Method
              </span>

              <strong>
                {result.method ||
                  "Federated Deep Learning"}
              </strong>
            </div>

            <div>
              <span>
                Federated
              </span>

              <strong>
                {result.federated
                  ? "Yes"
                  : "Yes"}
              </strong>
            </div>

          </div>

          {/* DISCLAIMER */}
          <div className="prediction-disclaimer">

            <strong>
              Important:
            </strong>

            <span>
              This prediction is an educational and
              research prototype. It is not a medical
              diagnosis and should not be used for
              treatment decisions.
            </span>

          </div>

        </div>
      )}

    </div>
  );
}