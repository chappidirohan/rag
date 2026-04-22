import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in [".docx", ".doc"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported extension: {ext}")
    
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    for chunk in chunks:
        chunk.metadata["source"] = os.path.basename(file_path).split("_", 1)[-1]
        
    return chunks
