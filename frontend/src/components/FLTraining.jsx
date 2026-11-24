import React, { useState } from "react";

const API = "http://127.0.0.1:5000/api";

const diseases = [
  "Diabetes",
  "Hypertension",
  "Heart Disease",
  "Kidney Disease",
  "Liver Disease",
  "Tuberculosis",
];

const hospitals = [
  "Hospital A",
  "Hospital B",
  "Hospital C",
  "Hospital D",
];

function FLTraining() {
  const [rounds, setRounds] = useState(5);
  const [training, setTraining] = useState(false);
  const [currentRound, setCurrentRound] = useState(0);
  const [metrics, setMetrics] = useState([]);
  const [message, setMessage] = useState("");

  const startTraining = async () => {
    setTraining(true);
    setCurrentRound(0);
    setMetrics([]);
    setMessage("Starting federated training...");

    try {
      const response = await fetch(
        `${API}/federated/train`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            rounds: Number(rounds),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message ||
          "Federated training failed."
        );
      }

      setMessage(
        "Federated training completed successfully."
      );

      if (data.metrics) {
        setMetrics(data.metrics);
      }

      setCurrentRound(Number(rounds));

    } catch (error) {
      console.error(error);

      setMessage(
        error.message ||
        "Unable to start federated training."
      );
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="page-container">

      {/* ================================================== */}
      {/* HEADER */}
      {/* ================================================== */}

      <div className="page-header">

        <div>
          <h1>Federated Learning</h1>

          <p>
            Privacy-preserving multi-hospital
            collaborative model training
          </p>
        </div>

      </div>


      {/* ================================================== */}
      {/* SYSTEM OVERVIEW */}
      {/* ================================================== */}

      <div className="card">

        <div className="card-header">

          <div>
            <h2>
              Multi-Hospital Federated Architecture
            </h2>

            <p>
              Hospitals train models locally without
              sharing patient data.
            </p>
          </div>

        </div>


        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(4, 1fr)",
            gap: "16px",
            marginTop: "20px",
          }}
        >

          {hospitals.map(
            (hospital, index) => (

              <div
                key={hospital}
                className="stat-card"
                style={{
                  textAlign: "center",
                }}
              >

                <div
                  style={{
                    fontSize: "30px",
                    marginBottom: "8px",
                  }}
                >
                  🏥
                </div>

                <h3>
                  {hospital}
                </h3>

                <p>
                  Local Dataset
                </p>

                <span
                  style={{
                    fontSize: "12px",
                    fontWeight: "600",
                  }}
                >
                  Patient data remains local
                </span>

              </div>

            )
          )}

        </div>


        {/* FEDERATED FLOW */}

        <div
          style={{
            marginTop: "28px",
            padding: "20px",
            borderRadius: "12px",
            background:
              "rgba(99, 102, 241, 0.08)",
          }}
        >

          <h3
            style={{
              textAlign: "center",
              marginBottom: "20px",
            }}
          >
            Federated Training Workflow
          </h3>


          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "14px",
              flexWrap: "wrap",
            }}
          >

            <div className="workflow-step">
              <strong>🏥 Hospitals</strong>
              <span>Local Data</span>
            </div>

            <div className="workflow-arrow">
              →
            </div>

            <div className="workflow-step">
              <strong>🧠 Local Training</strong>
              <span>Train locally</span>
            </div>

            <div className="workflow-arrow">
              →
            </div>

            <div className="workflow-step">
              <strong>📤 Model Updates</strong>
              <span>Parameters only</span>
            </div>

            <div className="workflow-arrow">
              →
            </div>

            <div className="workflow-step">
              <strong>⚙️ FedAvg</strong>
              <span>Aggregate</span>
            </div>

            <div className="workflow-arrow">
              →
            </div>

            <div className="workflow-step">
              <strong>🌐 Global Model</strong>
              <span>Shared model</span>
            </div>

          </div>

        </div>

      </div>


      {/* ================================================== */}
      {/* TRAINING CONFIGURATION */}
      {/* ================================================== */}

      <div className="card">

        <div className="card-header">

          <div>

            <h2>
              Federated Training Configuration
            </h2>

            <p>
              Configure the number of federated
              communication rounds.
            </p>

          </div>

        </div>


        <div
          style={{
            display: "flex",
            gap: "20px",
            alignItems: "end",
            flexWrap: "wrap",
            marginTop: "20px",
          }}
        >

          <div
            style={{
              minWidth: "220px",
            }}
          >

            <label>
              Federated Rounds
            </label>

            <input
              type="number"
              min="1"
              max="20"
              value={rounds}
              disabled={training}
              onChange={(e) =>
                setRounds(e.target.value)
              }
            />

          </div>


          <button
            className="primary-button"
            onClick={startTraining}
            disabled={training}
          >

            {training
              ? "Training..."
              : "Start Federated Training"}

          </button>

        </div>


        {message && (

          <div
            style={{
              marginTop: "18px",
              padding: "12px 16px",
              borderRadius: "8px",
              background:
                "rgba(99, 102, 241, 0.08)",
            }}
          >
            {message}
          </div>

        )}

      </div>


      {/* ================================================== */}
      {/* TRAINING PROGRESS */}
      {/* ================================================== */}

      <div className="card">

        <div className="card-header">

          <div>

            <h2>
              Training Progress
            </h2>

            <p>
              Federated communication rounds
            </p>

          </div>

        </div>


        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(3, 1fr)",
            gap: "16px",
            marginTop: "20px",
          }}
        >

          <div className="stat-card">

            <span>
              Current Round
            </span>

            <strong>
              {currentRound} / {rounds}
            </strong>

          </div>


          <div className="stat-card">

            <span>
              Hospital Nodes
            </span>

            <strong>
              4
            </strong>

          </div>


          <div className="stat-card">

            <span>
              Training Status
            </span>

            <strong>
              {training
                ? "Running"
                : currentRound ===
                    Number(rounds) &&
                  currentRound !== 0
                ? "Completed"
                : "Ready"}
            </strong>

          </div>

        </div>


        {/* PROGRESS BAR */}

        <div
          style={{
            marginTop: "24px",
          }}
        >

          <div
            style={{
              display: "flex",
              justifyContent:
                "space-between",
              marginBottom: "8px",
            }}
          >

            <span>
              Federated Progress
            </span>

            <span>
              {rounds > 0
                ? Math.round(
                    (currentRound /
                      Number(rounds)) *
                      100
                  )
                : 0}
              %
            </span>

          </div>


          <div
            style={{
              width: "100%",
              height: "10px",
              background:
                "rgba(128,128,128,0.18)",
              borderRadius: "10px",
              overflow: "hidden",
            }}
          >

            <div
              style={{
                width: `${
                  rounds > 0
                    ? Math.min(
                        (currentRound /
                          Number(rounds)) *
                          100,
                        100
                      )
                    : 0
                }%`,
                height: "100%",
                background:
                  "currentColor",
                borderRadius: "10px",
                transition:
                  "width 0.4s ease",
              }}
            />

          </div>

        </div>

      </div>


      {/* ================================================== */}
      {/* DISEASE MODELS */}
      {/* ================================================== */}

      <div className="card">

        <div className="card-header">

          <div>

            <h2>
              Federated Disease Models
            </h2>

            <p>
              Six disease-specific models trained
              across distributed hospital nodes.
            </p>

          </div>

        </div>


        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(3, 1fr)",
            gap: "16px",
            marginTop: "20px",
          }}
        >

          {diseases.map(
            (disease) => (

              <div
                key={disease}
                className="stat-card"
              >

                <div
                  style={{
                    display: "flex",
                    justifyContent:
                      "space-between",
                    alignItems: "center",
                    gap: "10px",
                  }}
                >

                  <h3>
                    {disease}
                  </h3>

                  <span
                    style={{
                      fontSize: "12px",
                      padding:
                        "5px 9px",
                      borderRadius:
                        "20px",
                      background:
                        "rgba(34,197,94,0.12)",
                      fontWeight: "600",
                    }}
                  >
                    Federated
                  </span>

                </div>


                <p
                  style={{
                    marginTop: "10px",
                  }}
                >
                  {disease ===
                  "Tuberculosis"
                    ? "CNN"
                    : "MLP"}
                </p>

                <p
                  style={{
                    fontSize: "13px",
                  }}
                >
                  4 hospital nodes
                </p>

              </div>

            )
          )}

        </div>

      </div>


      {/* ================================================== */}
      {/* METRICS */}
      {/* ================================================== */}

      {metrics.length > 0 && (

        <div className="card">

          <div className="card-header">

            <div>

              <h2>
                Federated Training Metrics
              </h2>

              <p>
                Performance recorded during
                federated communication rounds.
              </p>

            </div>

          </div>


          <div
            style={{
              overflowX: "auto",
              marginTop: "20px",
            }}
          >

            <table
              style={{
                width: "100%",
                borderCollapse:
                  "collapse",
              }}
            >

              <thead>

                <tr>

                  <th>
                    Round
                  </th>

                  <th>
                    Accuracy
                  </th>

                  <th>
                    Precision
                  </th>

                  <th>
                    Recall
                  </th>

                  <th>
                    F1 Score
                  </th>

                  <th>
                    ROC-AUC
                  </th>

                </tr>

              </thead>


              <tbody>

                {metrics.map(
                  (metric, index) => (

                    <tr
                      key={index}
                    >

                      <td>
                        {metric.round ??
                          index + 1}
                      </td>

                      <td>
                        {formatMetric(
                          metric.accuracy
                        )}
                      </td>

                      <td>
                        {formatMetric(
                          metric.precision
                        )}
                      </td>

                      <td>
                        {formatMetric(
                          metric.recall
                        )}
                      </td>

                      <td>
                        {formatMetric(
                          metric.f1
                        )}
                      </td>

                      <td>
                        {formatMetric(
                          metric.roc_auc
                        )}
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        </div>

      )}


      {/* ================================================== */}
      {/* PRIVACY NOTE */}
      {/* ================================================== */}

      <div
        className="card"
        style={{
          marginBottom: "30px",
        }}
      >

        <h2>
          🔐 Privacy-Preserving Design
        </h2>

        <p>
          Each hospital keeps its patient data
          locally. The federated learning process
          exchanges model parameters or updates
          rather than raw patient records. The
          central server aggregates the local
          updates using Federated Averaging (FedAvg)
          to create a shared global model.
        </p>

        <p
          style={{
            marginTop: "10px",
            fontSize: "13px",
          }}
        >
          Note: This is an educational and research
          prototype. Federated learning alone does
          not guarantee complete privacy or security.
        </p>

      </div>

    </div>
  );
}


/* ======================================================== */
/* FORMAT METRICS */
/* ======================================================== */

function formatMetric(value) {

  if (
    value === undefined ||
    value === null ||
    Number.isNaN(Number(value))
  ) {
    return "—";
  }

  const number = Number(value);

  if (number <= 1) {
    return `${(number * 100).toFixed(2)}%`;
  }

  return `${number.toFixed(2)}%`;
}


export default FLTraining;