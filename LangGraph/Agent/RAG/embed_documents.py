"""One-time ingestion script: builds the persistent Chroma vector store for the RAG agent.

Loads `iso27001.pdf` (expected to sit next to this file), splits it into
chunks, embeds them with Gemini embeddings, and persists the result to
`chroma_db/` (also next to this file). Run this once whenever the source
PDF changes or the vector store doesn't exist yet — `RAG_Agent.py` only
reads what this script produces, so you don't have to redo embedding every
time you want to talk to the document.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_dir, "iso27001.pdf")
persist_directory = os.path.join(base_dir, "chroma_db")
collection_name = "iso27001"

# Our Embedding Model - Groq (the LLM's provider) has no embeddings API,
# so this uses Google's Gemini embeddings instead (needs GOOGLE_API_KEY in .env).
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
)


# Safety measure I have put for debugging purposes :)
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path) # This loads the PDF

# Checks if the PDF is there
try:
    pages = pdf_loader.load()
    print(f"PDF has been loaded and has {len(pages)} pages")
except Exception as e:
    print(f"Error loading PDF: {e}")
    raise

# Chunking Process
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


pages_split = text_splitter.split_documents(pages) # We now apply this to our pages

# If our collection does not exist in the directory, we create using the os command
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)


try:
    # Here, we actually create the chroma database using our embeddigns model
    vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vector store!")

except Exception as e:
    print(f"Error setting up ChromaDB: {str(e)}")
    raise

print(f"Vector store ready at {persist_directory} — run RAG_Agent.py to talk to it without re-embedding.")
