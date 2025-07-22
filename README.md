# genai-sql-agent

AI-powered API to convert natural language questions into SQL queries for e-commerce datasets using FastAPI and a locally hosted Llama 3 model (via Ollama).

## 📦 Project structure

```
genai-sql-agent/
├── dataset/
│   ├── Product_level_ad_sales.csv
│   ├── Product_level_eligibility.csv
│   └── Product_level_total_sales.csv
├── results/
│   ├── pic_1_API_interface.png
│   ├── QUERY_RESULT1.png
│   └── QUERY_RESULT2.png
├── scripts/
│   ├── ecommerce.db
│   ├── GenAi.py
│   └── GenAi.ipynb
├── .gitignore
├── LICENSE
├── README.md
```

## 🚀 Project overview

This project provides a REST API that allows users to submit plain English questions about an e-commerce dataset. The system uses:

1️⃣ **Llama 3 (Ollama) for natural language to SQL translation**  
2️⃣ **SQLite as the database backend**  
3️⃣ **FastAPI for the REST interface**

## 🛠️ Setup and installation

### 1️⃣ Install Python dependencies:
```bash
pip install fastapi uvicorn requests
```

### 2️⃣ Install and set up Ollama:
- Download Ollama: [https://ollama.ai/download](https://ollama.ai/download)
- Pull and run a model (e.g. llama3):
  ```bash
  ollama pull llama3
  ollama serve
  ```

## ▶️ Running the API

Navigate to the `scripts/` directory and start FastAPI:

```bash
uvicorn GenAi:app --reload
```

Then access the API at:
- Root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc UI: `http://127.0.0.1:8000/redoc`

## 🔔 Example usage

POST `/query` with:
```json
{
  "question": "What is the average ad_sales value?"
}
```

Example response:
```json
{
  "received_question": "What is the average ad_sales value?",
  "generated_sql": "SELECT AVG(ad_sales) FROM pl_ad_sales;",
  "result": [
    { "AVG(ad_sales)": 245.75 }
  ]
}
```

## 📂 Explanation of repository contents

- `dataset/`: Source CSV files
- `results/`: Screenshots of API UI and example results
- `scripts/`: Main code, DB, and notebook
- `ecommerce.db`: SQLite DB containing 3 tables
  - `pl_total_sales`
  - `pl_ad_sales`
  - `pl_eligibility`

## 🔧 Features

- **Fully local, private execution**  
- **Schema-aware prompt to guide Llama 3 precisely**  
- **Clean JSON API interface with Swagger UI**

## 📄 License

MIT License — see `LICENSE` for details.
