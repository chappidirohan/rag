import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import uuid
import logging

# Import local modules
from processor import process_file
from vector_store import add_to_vector_store, query_vector_store
from llm_service import generate_answer

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG AI Service")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        chunks = process_file(file_path)
        add_to_vector_store(chunks, file.filename)
        
        return {"message": f"Successfully processed {file.filename}", "file_id": file_id}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        context_chunks = query_vector_store(request.query, k=request.top_k)
        if not context_chunks:
            return QueryResponse(answer="I don't know.", sources=[])
        
        answer = generate_answer(request.query, context_chunks)
        sources = list(set([chunk.metadata.get("source", "Unknown") for chunk in context_chunks]))
        
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
