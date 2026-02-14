from fastapi import FastAPI, UploadFile, File
import shutil
import os

from app.ingest import ingest_pdf
from app.rag import ask_question

from app.decision import evaluate_loan
from fastapi import Body

from app.crew_decision import run_crew_decision

app = FastAPI(title="AI Business Copilot")

DOCS_DIR = "data/documents"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-doc")
def upload_doc(file: UploadFile = File(...)):
    file_path = os.path.join(DOCS_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_pdf(file_path)

    return {"message": f"{file.filename} ingested successfully"}


@app.post("/ask")
def ask(q: str):
    answer = ask_question(q)
    return {"answer": answer}

@app.post("/decision")
def decision(data: dict = Body(...)):
    return evaluate_loan(data)

@app.post("/crew-decision")
def crew_decision(data: dict):
    return run_crew_decision(data)