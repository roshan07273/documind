from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

def ingest_pdf(file_path: str):
    print("Loading PDF...")
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    print(f"Loaded {len(pages)} pages")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)
    print(f"Split into {len(chunks)} chunks")

    embeddings = FakeEmbeddings(size=384)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("FAISS index ready!")
    return vectorstore
