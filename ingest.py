import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document  # Ensure correct doc format
from uuid import uuid4
from models import Models

load_dotenv()

# Initialize models
models = Models()
embeddings = models.embeddings_ollama
llm = models.model_ollama

# Constants
DATA_FOLDER = "./data"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 50
CHUNK_INTERVAL = 10  # Seconds
VECTOR_DB_PATH = "./db/chroma_langchain_db"

# Initialize Chroma vector store
vector_store = Chroma(
    collection_name="cricket-documents",
    embedding_function=embeddings,
    persist_directory=VECTOR_DB_PATH,
)

# Ingest a file into ChromaDB
def ingest_file(file_path):
    if not file_path.lower().endswith('.txt'):
        print(f"Skipping non-text file: {file_path}")
        return

    print(f"Starting ingestion: {file_path}")

    # Load text
    loader = TextLoader(file_path, encoding="utf-8")
    loaded_documents = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " "],  # Remove empty separator
    )
    documents = text_splitter.split_documents(loaded_documents)

    if not documents:
        print(f"No valid content found in {file_path}. Skipping...")
        return

    # Convert to Chroma format
    chroma_docs = [Document(page_content=doc.page_content, metadata={"source": file_path}) for doc in documents]

    # Generate unique IDs for each chunk
    uuids = [str(uuid4()) for _ in chroma_docs]

    # Add documents to ChromaDB
    print(f"Adding {len(chroma_docs)} chunks to vector store...")
    vector_store.add_documents(chroma_docs, ids=uuids)

    print(f"Finished ingesting {file_path}")

# Main loop: Monitor folder and ingest files
def main_loop():
    while True:
        for filename in os.listdir(DATA_FOLDER):
            if not filename.startswith("_"):  # Ignore already processed files
                file_path = os.path.join(DATA_FOLDER, filename)
                ingest_file(file_path)

                # Rename file after processing to avoid re-ingestion
                try:
                    new_filename = f"_{filename}"
                    os.rename(file_path, os.path.join(DATA_FOLDER, new_filename))
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")

                # Delete temporary or error files
                for file in os.listdir(DATA_FOLDER):
                    if file.startswith("_"):
                        try:
                            os.remove(os.path.join(DATA_FOLDER, file))
                        except Exception as e:
                            print(f"Error deleting {file}: {e}")

        time.sleep(CHUNK_INTERVAL)  # Wait before rechecking folder

# Run the script
if __name__ == "__main__":
    main_loop()
