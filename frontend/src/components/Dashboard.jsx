import React from "react";

export default function Dashboard() {
  return (
    <section>
      <div className="cards">
        <div className="card"><span>Simulated Hospitals</span><strong>4</strong></div>
        <div className="card"><span>Raw Data Shared</span><strong>NO</strong></div>
        <div className="card"><span>Federated Method</span><strong>FedAvg</strong></div>
        <div className="card"><span>AI Modules</span><strong>4</strong></div>
      </div>

      <div className="panel">
        <h3>System Architecture</h3>
        <div className="flow">
          {['Hospital A','Hospital B','Hospital C','Hospital D'].map((name) => (
            <div key={name}><b>{name}</b><small>Local data + model</small></div>
          ))}
          <div className="server"><b>Federated Server</b><small>FedAvg parameter aggregation</small></div>
        </div>
      </div>

      <div className="panel">
        <h3>Project Components</h3>
        <ul>
          <li>Machine learning risk prediction</li>
          <li>Federated averaging across four simulated hospitals</li>
          <li>NLP extraction from clinical text</li>
          <li>Optional hosted LLM explanation with local fallback</li>
          <li>React + Flask full-stack dashboard</li>
        </ul>
      </div>
    </section>
  );
}
