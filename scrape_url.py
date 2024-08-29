import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

def fetch_and_persist_article(url):
    messages = []
    local_embeddings = get_embedding_function()


    if os.path.exists(CHROMA_PATH):
        vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=local_embeddings)
        messages.append("Loaded the existing Chroma DB")
    else:
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=local_embeddings
        )
        messages.append("Created the Chroma DB")

    loader = WebBaseLoader(url)
    messages.append("URL loaded")

    data = loader.load()

    text_splitter =  RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectorstore.add_documents(documents=all_splits)
    messages.append("Added to Chroma DB")

    return messages
