# DocuMind 🧠 — RAG-Powered Document Q&A

> Upload any PDF and ask natural language questions against it.  
> Built with **LangChain** · **FAISS** · **Groq LLM** · **FastAPI**

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://documind.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-latest-orange)](https://langchain.com)

---

## 🚀 Live Demo

**API Docs:** [https://documind.onrender.com/docs](documind-1-r4ne.onrender.com/docs)

---

## 🏗️ Architecture

```
PDF Upload
    ↓
PyPDFLoader  →  Text Extraction
    ↓
RecursiveCharacterTextSplitter  →  1000-char chunks (200 overlap)
    ↓
FakeEmbeddings / OpenAI Embeddings
    ↓
FAISS Vector Index  ←→  Similarity Search (top-4 chunks)
    ↓
User Question  →  LangChain RAG Chain
    ↓
Groq LLM (llama-3.3-70b-versatile)
    ↓
Answer + Source Pages
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| API Framework | FastAPI + Uvicorn | REST endpoints + async server |
| PDF Parsing | PyPDF | Extract text from PDF pages |
| Text Chunking | LangChain RecursiveCharacterTextSplitter | Split text into overlapping chunks |
| Vector Store | FAISS (Facebook AI Similarity Search) | Store & search embeddings |
| LLM | Groq (llama-3.3-70b-versatile) | Generate answers |
| RAG Chain | LangChain LCEL | Connect retriever + LLM |
| Deployment | Render.com | Free cloud hosting |

---

## 📁 Project Structure

```
documind/
├── main.py              # FastAPI app — routes & session management
├── app/
│   ├── __init__.py
│   ├── ingest.py        # PDF → chunks → FAISS vector store
│   └── rag.py           # LangChain RAG chain with Groq LLM
├── uploads/             # Temporary PDF storage (gitignored)
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/roshan07273/documind.git
cd documind
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add environment variables
```bash
cp .env.example .env
# Add your GROQ_API_KEY (free at console.groq.com)
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

Open: **http://localhost:8000/docs**

---

## 🔌 API Endpoints

### `GET /`
Health check.
```json
{ "message": "DocuMind is running!" }
```

### `POST /upload`
Upload a PDF file.
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```
**Response:**
```json
{
  "session_id": "document",
  "message": "Ready! Now ask questions."
}
```

### `POST /ask`
Ask a question against the uploaded document.
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"session_id": "document", "question": "What is this about?"}'
```
**Response:**
```json
{
  "answer": "This document is about..."
}
```

### `GET /sessions`
List all active sessions.

### `DELETE /session/{session_id}`
Clear a session from memory.

---

## 🧠 How RAG Works

1. **Ingest** — PDF parsed page by page, split into 1000-char overlapping chunks
2. **Embed** — Each chunk converted to a vector (numerical representation)
3. **Index** — Vectors stored in FAISS for fast similarity search
4. **Retrieve** — User question embedded; top-4 most similar chunks retrieved
5. **Generate** — Groq LLM answers using only those chunks as context
6. **Return** — Answer sent back to the user

---

## 🌐 Deployment

Deployed on **Render.com** (free tier):
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
- Environment Variable: `GROQ_API_KEY`

---

## 👤 Author

**Roshan Raturi**  
[LinkedIn](https://www.linkedin.com/in/roshanraturi28/) · [GitHub](https://github.com/roshan07273) · [LeetCode](https://leetcode.com/u/roshanraturi07/)
