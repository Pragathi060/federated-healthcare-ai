import React, { useEffect, useState } from "react";

import Dashboard from "./components/Dashboard";
import Prediction from "./components/Prediction";
import Hospitals from "./components/Hospitals";
import FLTraining from "./components/FLTraining";
import NLPAnalysis from "./components/NLPAnalysis";
import LLMAssistant from "./components/LLMAssistant";
import ModelPerformance from "./components/ModelPerformance";

const API = "http://127.0.0.1:5000/api";

export default function App() {
  const [page, setPage] = useState("dashboard");
  const [health, setHealth] = useState("Checking...");

  useEffect(() => {
    checkBackend();

    const interval = setInterval(() => {
      checkBackend();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const checkBackend = () => {
    fetch(`${API}/health`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend unavailable");
        }

        return response.json();
      })
      .then(() => {
        setHealth("Backend connected");
      })
      .catch(() => {
        setHealth("Backend offline");
      });
  };

  const props = {
    api: API,
  };

  const pages = {
    dashboard: <Dashboard {...props} />,

    prediction: <Prediction {...props} />,

    hospitals: <Hospitals {...props} />,

    federated: <FLTraining {...props} />,

    modelPerformance: <ModelPerformance {...props} />,

    nlp: <NLPAnalysis {...props} />,

    llm: <LLMAssistant {...props} />,
  };

  const navigation = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: "⌂",
    },
    {
      id: "prediction",
      label: "Disease Prediction",
      icon: "⚕",
    },
    {
      id: "hospitals",
      label: "Hospital Nodes",
      icon: "🏥",
    },
    {
      id: "federated",
      label: "Federated Training",
      icon: "🔗",
    },
    {
      id: "modelPerformance",
      label: "Model Performance",
      icon: "📊",
    },
    {
      id: "nlp",
      label: "NLP Report Analyzer",
      icon: "📝",
    },
    {
      id: "llm",
      label: "AI Assistant",
      icon: "🤖",
    },
  ];

  return (
    <div className="app">

      {/* SIDEBAR */}
      <aside className="sidebar">

        {/* BRAND */}
        <div className="brand">
          <h1>Federated AI</h1>

          <p className="subtitle">
            Healthcare Prototype
          </p>
        </div>


        {/* NAVIGATION */}
        <nav className="navigation">

          {navigation.map((item) => (
            <button
              key={item.id}
              className={`nav-button ${
                page === item.id ? "active" : ""
              }`}
              onClick={() => setPage(item.id)}
            >

              <span className="nav-icon">
                {item.icon}
              </span>

              <span>
                {item.label}
              </span>

            </button>
          ))}

        </nav>


        {/* BACKEND CONNECTION */}
        <div className="connection-card">

          <div className="connection-title">
            Backend Status
          </div>

          <div
            className={`connection ${
              health === "Backend connected"
                ? "online"
                : "offline"
            }`}
          >

            <span className="status-dot">
              ●
            </span>

            {health}

          </div>

        </div>

      </aside>


      {/* MAIN CONTENT */}
      <main className="main">

        {/* HEADER */}
        <header className="main-header">

          <div>

            <h2>
              Privacy-Preserving Multi-Hospital AI
            </h2>

            <p>
              Federated Learning + Deep Learning + NLP + LLM
            </p>

          </div>


          <div className="system-badge">

            <span>
              ●
            </span>

            AI Research Prototype

          </div>

        </header>


        {/* PAGE CONTENT */}
        <section className="page-content">

          {pages[page]}

        </section>


        {/* FOOTER */}
        <footer>

          <strong>
            Federated Healthcare AI
          </strong>

          <span>
            Educational and research prototype only.
            Not a medical diagnosis or treatment system.
          </span>

        </footer>

      </main>

    </div>
  );
}
