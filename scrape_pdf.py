import os
import shutil
import hashlib
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma

CHROMA_PATH = "chroma"
DATA_PATH = "pdf_files"
HASHES_PATH = "pdf_hashes"
ALLOWED_EXTENSIONS = {'pdf'}

# Crear directorios para los datos y hashes si no existen
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(HASHES_PATH, exist_ok=True)


def allowed_file(filename):
    """Check if the file has a valid PDF extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_file_hash(file):
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    file.seek(0)  # Ensure the file pointer is at the start
    for chunk in iter(lambda: file.read(4096), b""):
        hash_sha256.update(chunk)
    file.seek(0)  # Reset the file pointer after reading
    return hash_sha256.hexdigest()


def is_duplicate(file_hash):
    """Check if the file hash already exists in the stored hashes."""
    hash_file_path = os.path.join(HASHES_PATH, file_hash)
    return os.path.exists(hash_file_path)


def save_file(file):
    """Save uploaded file to the data directory."""
    file_hash = calculate_file_hash(file)
    if is_duplicate(file_hash):
        return None, "Archivo ya existe"

    filename = secure_filename(file.filename)
    file_path = os.path.join(DATA_PATH, filename)
    file.save(file_path)

    # Store the hash in a file to mark it as seen
    with open(os.path.join(HASHES_PATH, file_hash), 'w') as f:
        f.write(filename)

    return file_path, None


def load_documents():
    """Load documents from the data directory."""
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    """Add document chunks to Chroma database."""
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    chunks_with_ids = calculate_chunk_ids(chunks)
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add")

def calculate_chunk_ids(chunks):
    """Calculate and assign IDs to document chunks."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

def clear_database():
    """Clear the Chroma database."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
