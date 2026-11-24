import React, { useEffect, useState } from "react";

export default function Hospitals({ api }) {
  const [hospitals, setHospitals] = useState([]);
  useEffect(() => {
    fetch(`${api}/hospitals`).then((r) => r.json()).then((d) => setHospitals(d.hospitals || []));
  }, [api]);

  return (
    <section className="panel">
      <h3>Hospital Nodes</h3>
      <div className="hospital-grid">
        {hospitals.map((hospital) => (
          <div className="hospital" key={hospital.id}>
            <h4>{hospital.name}</h4>
            <p>{hospital.status}</p>
            <div>Raw patient data shared: <b>NO</b></div>
            <div>Model parameters shared: <b>YES</b></div>
          </div>
        ))}
      </div>
    </section>
  );
}
