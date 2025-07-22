from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import sqlite3

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "API is running ✅"}

def generate_sql_from_question(question):
    prompt = f"""
    You are an expert SQL assistant working with SQLite. Below are the exact table schemas you should use to write queries.
    
    1️⃣ Table `pl_total_sales`:
    - date (TEXT, format: dd-mm-yyyy)
    - item_id (INTEGER)
    - total_sales (REAL)
    - total_units_sold (INTEGER)

    2️⃣ Table `pl_ad_sales`:
    - date (TEXT, format: dd-mm-yyyy)
    - item_id (INTEGER)
    - ad_sales (REAL)
    - impressions (INTEGER)
    - ad_spend (REAL)
    - clicks (INTEGER)
    - units_sold (INTEGER)

    3️⃣ Table `pl_eligibility`:
    - eligibility_check_date (TEXT, format: dd-mm-yyyy)
    - item_id (INTEGER)
    - eligibility (TEXT, 'TRUE' or 'FALSE')
    - message (TEXT)

    🎯 Instructions:
    - Only use these columns and table names exactly as defined.
    - Do not use placeholders like '?' or ':param'.
    - Do not include Markdown formatting or explanation.
    - Always output a **complete valid SQLite SQL query**.

    The user question is:
    {question}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    sql = data.get("response", "").strip()
    sql = sql.replace('```', '').strip()  # Clean up any markdown just in case
    return sql



def execute_sql_query(sql_query):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.post("/query")
async def query(request: QueryRequest):
    sql_query = generate_sql_from_question(request.question)
    result = execute_sql_query(sql_query)
    return {
        "received_question": request.question,
        "generated_sql": sql_query,
        "result": result
    }
