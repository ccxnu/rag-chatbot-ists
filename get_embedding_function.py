from langchain_community.embeddings.ollama import OllamaEmbeddings

OLLAMA_MODEL = "llama3.1:8b"

def get_embedding_function():
    embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
    return embeddings
