import React, { useState } from "react";

export default function NLPAnalysis({ api }) {
  const [text, setText] = useState(
    "Patient reports frequent urination, excessive thirst and fatigue. Glucose: 145."
  );

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${api}/nlp/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Analysis failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel">
      <h3>NLP Medical Report Analyzer</h3>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows="7"
        placeholder="Enter a medical report..."
      />

      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Report"}
      </button>

      {error && (
        <div className="result">
          <p>{error}</p>
        </div>
      )}

      {result && result.nlp_analysis && (
        <div className="result">

          {/* ================================
              DETECTED SYMPTOMS
          ================================= */}

          <h4>Detected Symptoms</h4>

          {result.nlp_analysis.symptoms?.length > 0 ? (
            <ul>
              {result.nlp_analysis.symptoms.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          ) : (
            <p>No symptoms detected.</p>
          )}


          {/* ================================
              DETECTED CONDITIONS
          ================================= */}

          <h4>Detected Conditions</h4>

          {result.nlp_analysis.conditions?.length > 0 ? (
            <ul>
              {result.nlp_analysis.conditions.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          ) : (
            <p>No conditions detected.</p>
          )}


          {/* ================================
              MEDICATIONS
          ================================= */}

          <h4>Medications</h4>

          {result.nlp_analysis.medications?.length > 0 ? (
            <ul>
              {result.nlp_analysis.medications.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          ) : (
            <p>No medications detected.</p>
          )}


          {/* ================================
              MEASUREMENTS
          ================================= */}

          <h4>Measurements</h4>

          {Object.keys(result.nlp_analysis.measurements || {}).length > 0 ? (
            <ul>
              {Object.entries(result.nlp_analysis.measurements).map(
                ([key, value]) => (
                  <li key={key}>
                    <strong>{key}:</strong> {value}
                  </li>
                )
              )}
            </ul>
          ) : (
            <p>No measurements detected.</p>
          )}


          {/* ==========================================
              POSSIBLE DISEASE INDICATORS
          =========================================== */}

          <h4>Possible Disease Indicators</h4>

          {result.disease_predictions &&
          result.disease_predictions.length > 0 ? (

            <div className="disease-predictions">

              {result.disease_predictions.map((item, index) => (
                <div
                  key={index}
                  className="disease-prediction"
                >

                  <h4>
                    {item.disease}
                  </h4>

                  <p>
                    <strong>Indicator:</strong>{" "}
                    {item.level}
                  </p>

                  <p>
                    {item.message}
                  </p>

                  {item.evidence &&
                    item.evidence.length > 0 && (
                      <p>
                        <strong>
                          Supporting findings:
                        </strong>{" "}
                        {item.evidence.join(", ")}
                      </p>
                    )}

                </div>
              ))}

            </div>

          ) : (

            <p>
              No strong disease indicators were identified
              from the information provided.
            </p>

          )}


          {/* ==========================================
              AI CLINICAL EXPLANATION
          =========================================== */}

          <h4>AI Clinical Explanation</h4>

          <p>
            {result.llm_explanation}
          </p>


          {/* ==========================================
              DISCLAIMER
          =========================================== */}

          <p>
            <strong>Disclaimer:</strong>{" "}
            {result.disclaimer}
          </p>

        </div>
      )}
    </section>
  );
}
