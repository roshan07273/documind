
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ingest import ingest_pdf
from app.rag import get_rag_chain

app = FastAPI(title="DocuMind API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

vectorstores = {}

class QuestionRequest(BaseModel):
    session_id: str
    question: str

@app.get("/")
def root():
    return {"message": "DocuMind is running!"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    session_id = file.filename.replace(".pdf","").replace(" ","_")
    vectorstores[session_id] = ingest_pdf(file_path)
    return {"session_id": session_id, "message": "Ready! Now ask questions."}

@app.post("/ask")
def ask(req: QuestionRequest):
    if req.session_id not in vectorstores:
        raise HTTPException(status_code=404, detail="Upload a PDF first.")
    chain = get_rag_chain(vectorstores[req.session_id])
    answer = chain.invoke(req.question)
    return {"answer": answer}
