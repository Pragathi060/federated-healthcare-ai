# Federated Healthcare AI

A final academic prototype combining **Machine Learning, Federated Learning, NLP, and an optional LLM layer** for a simulated multi-hospital healthcare environment.

## Important scope
- This is an educational simulation, not a clinical product.
- The dataset is the public scikit-learn diabetes dataset.
- Four simulated hospital datasets are created from that public dataset.
- The `Outcome` label is created by comparing the original continuous target with its median.
- No real hospital patient records are included.
- The model output must not be used for diagnosis or treatment.

## Final project structure
```text
federated-healthcare-ai/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── api/
│   │   └── routes.py
│   ├── data/
│   │   ├── create_hospital_data.py
│   │   ├── hospital_a.csv
│   │   ├── hospital_b.csv
│   │   ├── hospital_c.csv
│   │   └── hospital_d.csv
│   ├── ml/
│   │   ├── model.py
│   │   ├── preprocess.py
│   │   └── train.py
│   ├── federated/
│   │   ├── fedavg.py
│   │   └── run_federated.py
│   ├── nlp/
│   │   └── processor.py
│   ├── llm/
│   │   └── assistant.py
│   └── models/
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── components/
│       │   ├── Dashboard.jsx
│       │   ├── Prediction.jsx
│       │   ├── Hospitals.jsx
│       │   ├── FLTraining.jsx
│       │   ├── NLPAnalysis.jsx
│       │   └── LLMAssistant.jsx
│       └── styles/
│           └── App.css
├── notebooks/
└── README.md
```

## Backend setup
Open PowerShell in the `backend` folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Generate the four hospital files:

```powershell
python -m data.create_hospital_data
```

Train the four local hospital models:

```powershell
python -m ml.train
```

Run the simulated FedAvg process:

```powershell
python -m federated.run_federated
```

Start Flask:

```powershell
python app.py
```

Backend URL: `http://127.0.0.1:5000`

## Frontend setup
Open a second PowerShell window from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

## What to demonstrate to the guide
1. **Dashboard** — four simulated hospitals and the privacy concept.
2. **Hospital Nodes** — raw data stays local; model parameters are shared.
3. **Federated Training** — run 5 rounds and show the metrics table.
4. **ML Risk Prediction** — enter standardized feature values and show the prediction.
5. **NLP Report Analyzer** — paste a short medical-style sentence and show extracted entities.
6. **AI Assistant** — generate a patient-friendly explanation.

## Optional real LLM
The project runs without an external LLM. To use a hosted Hugging Face text-generation model, set these environment variables before starting Flask:

```powershell
$env:HF_TOKEN="your_token_here"
$env:HF_MODEL="google/flan-t5-small"
python app.py
```

Do not send real patient records to an external LLM service. Use only synthetic or demonstration text.

## API endpoints
- `GET /api/health`
- `GET /api/hospitals`
- `GET /api/federated-metrics`
- `POST /api/federated/train`
- `POST /api/predict`
- `POST /api/nlp/analyze`
- `POST /api/llm/explain`
