import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import logging

logger = logging.getLogger(__name__)

CHROMA_PATH = "chroma_db"

def get_vector_store():
    """
    Initializes/returns the Chroma vector store using local HuggingFace embeddings.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    return vector_store

def add_to_vector_store(chunks, filename):
    """
    Adds chunks to the vector store.
    """
    logger.info(f"Adding {len(chunks)} chunks to vector store for {filename}")
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

def query_vector_store(query, k=3):
    """
    Retrieves most similar chunks from vector store.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results
