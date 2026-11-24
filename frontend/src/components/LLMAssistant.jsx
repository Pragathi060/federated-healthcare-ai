import React, { useState } from "react";

export default function LLMAssistant({ api }) {
  const [text, setText] = useState("Patient has high glucose and frequent urination. Explain this report in simple educational language.");
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    const response = await fetch(`${api}/llm/explain`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setAnswer(data.explanation || data.error || "No response");
  };

  return (
    <section className="panel">
      <h3>AI Clinical Assistant</h3>
      <p>Uses the optional hosted LLM when configured; otherwise the local educational fallback is used.</p>
      <textarea value={text} onChange={(e) => setText(e.target.value)} rows="7" />
      <button onClick={ask}>Generate Explanation</button>
      {answer && <div className="result"><p>{answer}</p></div>}
    </section>
  );
}
