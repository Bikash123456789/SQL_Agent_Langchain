# backend/main.py
import time
from fastapi import FastAPI
from pydantic import BaseModel
from .langchain_agent import run_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (like Streamlit) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryInput(BaseModel):
    question: str


@app.post("/query")
def get_sql_response(query: QueryInput):
    start = time.time()
    result = run_query(query.question)
    end = time.time()
    print(f"⏱️ Time taken: {round(end - start, 2)} seconds")
    return {"response": result}
