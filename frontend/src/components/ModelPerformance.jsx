import React from "react";

export default function ModelPerformance() {

  const models = [
    {
      disease: "Diabetes",
      model: "MLP",
      type: "Tabular",
      accuracy: 99.04,
      federated: true,
      hospitals: 4,
    },
    {
      disease: "Hypertension",
      model: "MLP",
      type: "Tabular",
      accuracy: 100.00,
      federated: true,
      hospitals: 4,
    },
    {
      disease: "Heart Disease",
      model: "MLP",
      type: "Tabular",
      accuracy: 81.67,
      federated: true,
      hospitals: 4,
    },
    {
      disease: "Kidney Disease",
      model: "MLP",
      type: "Tabular",
      accuracy: 100.00,
      federated: true,
      hospitals: 4,
    },
    {
      disease: "Liver Disease",
      model: "MLP",
      type: "Tabular",
      accuracy: 76.00,
      federated: true,
      hospitals: 4,
    },
    {
      disease: "Tuberculosis",
      model: "CNN",
      type: "Chest X-Ray",
      accuracy: 78.57,
      federated: true,
      hospitals: 4,
    },
  ];


  const averageAccuracy =
    models.reduce(
      (sum, item) => sum + item.accuracy,
      0
    ) / models.length;


  const bestModel = models.reduce(
    (best, item) =>
      item.accuracy > best.accuracy
        ? item
        : best,
    models[0]
  );


  return (
    <section>

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <div className="panel">

        <h3>
          AI Model Performance
        </h3>

        <p>
          Performance comparison of the six
          disease-specific deep learning models
          used in the privacy-preserving federated
          healthcare AI prototype.
        </p>

      </div>


      {/* ================================================= */}
      {/* SUMMARY CARDS */}
      {/* ================================================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(190px, 1fr))",
          gap: "16px",
          marginTop: "20px",
        }}
      >

        {/* TOTAL MODELS */}

        <div className="panel">

          <h4>
            Total Models
          </h4>

          <div
            style={{
              fontSize: "30px",
              fontWeight: "bold",
            }}
          >
            6
          </div>

          <p>
            Disease-specific models
          </p>

        </div>


        {/* MODEL TYPES */}

        <div className="panel">

          <h4>
            Model Types
          </h4>

          <div
            style={{
              fontSize: "30px",
              fontWeight: "bold",
            }}
          >
            2
          </div>

          <p>
            MLP + CNN
          </p>

        </div>


        {/* AVERAGE */}

        <div className="panel">

          <h4>
            Average Accuracy
          </h4>

          <div
            style={{
              fontSize: "30px",
              fontWeight: "bold",
            }}
          >
            {averageAccuracy.toFixed(2)}%
          </div>

          <p>
            Experimental evaluation
          </p>

        </div>


        {/* HOSPITALS */}

        <div className="panel">

          <h4>
            Hospital Nodes
          </h4>

          <div
            style={{
              fontSize: "30px",
              fontWeight: "bold",
            }}
          >
            4
          </div>

          <p>
            Simulated institutions
          </p>

        </div>


        {/* FEDERATED */}

        <div className="panel">

          <h4>
            Federated Models
          </h4>

          <div
            style={{
              fontSize: "30px",
              fontWeight: "bold",
            }}
          >
            6 / 6
          </div>

          <p>
            Models available
          </p>

        </div>


        {/* BEST MODEL */}

        <div className="panel">

          <h4>
            Highest Accuracy
          </h4>

          <div
            style={{
              fontSize: "22px",
              fontWeight: "bold",
            }}
          >
            {bestModel.accuracy.toFixed(2)}%
          </div>

          <p>
            {bestModel.disease}
          </p>

        </div>

      </div>


      {/* ================================================= */}
      {/* MODEL COMPARISON */}
      {/* ================================================= */}

      <div
        className="panel"
        style={{
          marginTop: "20px",
        }}
      >

        <h3>
          Federated Model Comparison
        </h3>

        <p>
          Each disease uses a separate model trained
          using distributed hospital data.
        </p>


        <div
          style={{
            overflowX: "auto",
            marginTop: "18px",
          }}
        >

          <table>

            <thead>

              <tr>

                <th>
                  Disease
                </th>

                <th>
                  Model
                </th>

                <th>
                  Data Type
                </th>

                <th>
                  Accuracy
                </th>

                <th>
                  Hospitals
                </th>

                <th>
                  Learning
                </th>

                <th>
                  Status
                </th>

              </tr>

            </thead>


            <tbody>

              {models.map(
                (item) => (

                  <tr
                    key={item.disease}
                  >

                    <td>
                      <strong>
                        {item.disease}
                      </strong>
                    </td>


                    <td>
                      {item.model}
                    </td>


                    <td>
                      {item.type}
                    </td>


                    <td>
                      <strong>
                        {item.accuracy.toFixed(2)}%
                      </strong>
                    </td>


                    <td>
                      {item.hospitals}
                    </td>


                    <td>
                      FedAvg
                    </td>


                    <td>

                      <span
                        style={{
                          padding:
                            "5px 10px",
                          borderRadius:
                            "12px",
                          background:
                            "#e8f5e9",
                          color:
                            "#2e7d32",
                          fontWeight:
                            "bold",
                          whiteSpace:
                            "nowrap",
                        }}
                      >
                        ● Federated
                      </span>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>


      {/* ================================================= */}
      {/* ACCURACY COMPARISON */}
      {/* ================================================= */}

      <div
        className="panel"
        style={{
          marginTop: "20px",
        }}
      >

        <h3>
          Accuracy Comparison
        </h3>

        <p>
          Experimental test-set accuracy of the
          disease prediction models.
        </p>


        <div
          style={{
            marginTop: "20px",
          }}
        >

          {models.map(
            (item) => (

              <div
                key={item.disease}
                style={{
                  marginBottom: "20px",
                }}
              >

                <div
                  style={{
                    display: "flex",
                    justifyContent:
                      "space-between",
                    marginBottom: "7px",
                  }}
                >

                  <strong>
                    {item.disease}
                  </strong>

                  <span>
                    {item.accuracy.toFixed(2)}%
                  </span>

                </div>


                <div
                  style={{
                    width: "100%",
                    height: "14px",
                    background:
                      "#e5e7eb",
                    borderRadius:
                      "10px",
                    overflow:
                      "hidden",
                  }}
                >

                  <div
                    style={{
                      width:
                        `${item.accuracy}%`,
                      height: "100%",
                      background:
                        "currentColor",
                      borderRadius:
                        "10px",
                      transition:
                        "width 0.4s ease",
                    }}
                  />

                </div>

              </div>

            )
          )}

        </div>

      </div>


      {/* ================================================= */}
      {/* MODEL ARCHITECTURE */}
      {/* ================================================= */}

      <div
        className="panel"
        style={{
          marginTop: "20px",
        }}
      >

        <h3>
          Model Architecture
        </h3>


        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "15px",
            marginTop: "18px",
          }}
        >

          {/* TABULAR */}

          <div className="status-card">

            <h4>
              Tabular Diseases
            </h4>

            <p>
              Diabetes, Hypertension, Heart Disease,
              Kidney Disease and Liver Disease.
            </p>

            <strong>
              MLP / Deep Neural Network
            </strong>

          </div>


          {/* TB */}

          <div className="status-card">

            <h4>
              Image Disease
            </h4>

            <p>
              Tuberculosis prediction using
              chest X-ray images.
            </p>

            <strong>
              CNN
            </strong>

          </div>


          {/* FEDERATED */}

          <div className="status-card">

            <h4>
              Federated Learning
            </h4>

            <p>
              Four simulated hospitals train
              locally without sharing raw
              patient data.
            </p>

            <strong>
              FedAvg
            </strong>

          </div>


          {/* GLOBAL */}

          <div className="status-card">

            <h4>
              Global Model
            </h4>

            <p>
              Local model updates are aggregated
              into a shared global model.
            </p>

            <strong>
              Federated Global Model
            </strong>

          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* FEDERATED WORKFLOW */}
      {/* ================================================= */}

      <div
        className="panel"
        style={{
          marginTop: "20px",
        }}
      >

        <h3>
          Federated Learning Workflow
        </h3>


        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "12px",
            flexWrap: "wrap",
            marginTop: "20px",
          }}
        >

          <div className="status-card">
            <strong>
              🏥 Hospital A
            </strong>
            <p>
              Local Training
            </p>
          </div>


          <span>
            →
          </span>


          <div className="status-card">
            <strong>
              🏥 Hospital B
            </strong>
            <p>
              Local Training
            </p>
          </div>


          <span>
            →
          </span>


          <div className="status-card">
            <strong>
              🏥 Hospital C
            </strong>
            <p>
              Local Training
            </p>
          </div>


          <span>
            →
          </span>


          <div className="status-card">
            <strong>
              🏥 Hospital D
            </strong>
            <p>
              Local Training
            </p>
          </div>


          <span>
            →
          </span>


          <div className="status-card">
            <strong>
              ⚙️ FedAvg
            </strong>
            <p>
              Aggregation
            </p>
          </div>


          <span>
            →
          </span>


          <div className="status-card">
            <strong>
              🌐 Global Model
            </strong>
            <p>
              Shared Model
            </p>
          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* EVALUATION NOTE */}
      {/* ================================================= */}

      <div
        className="panel"
        style={{
          marginTop: "20px",
          borderLeft:
            "5px solid #f59e0b",
        }}
      >

        <h3>
          Evaluation Note
        </h3>

        <p>
          The displayed results are experimental
          evaluation results obtained using the
          project datasets.
        </p>

        <p>
          They should not be interpreted as clinical
          accuracy or evidence of real-world medical
          performance.
        </p>

        <p>
          Dataset size, class distribution,
          preprocessing, model architecture and
          training conditions can affect these
          results.
        </p>

      </div>


      {/* ================================================= */}
      {/* PRIVACY NOTE */}
      {/* ================================================= */}

      <div
        className="panel"
        style={{
          marginTop: "20px",
          marginBottom: "30px",
        }}
      >

        <h3>
          🔐 Privacy-Preserving Design
        </h3>

        <p>
          Patient data remains within the individual
          hospital node during local training.
          Federated learning aggregates model
          updates rather than requiring raw patient
          records to be centrally collected.
        </p>

        <p
          style={{
            marginTop: "10px",
            fontSize: "13px",
          }}
        >
          This system is an educational and research
          prototype. Federated learning by itself does
          not guarantee complete privacy or security.
        </p>

      </div>

    </section>
  );
}