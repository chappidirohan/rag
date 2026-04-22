# Full-Stack RAG Application Setup Guide

This project consists of three main components:
1. **AI Service (FastAPI)**: Python service for document processing and RAG logic.
2. **Backend (Spring Boot)**: Java orchestrator for API routing and metadata.
3. **Frontend (React)**: Modern UI for users to upload and chat.

---

## 🚀 How to Run

### 1. AI Service (Python)
- Navigate to `ai-service/`
- Install dependencies: `pip install -r requirements.txt`
- Set your `OPENAI_API_KEY` in `.env`
- Run the service: `python main.py` (Runs on port 8000)

### 2. Backend (Spring Boot)
- Navigate to `backend/`
- Build the project: `mvn clean install` (requires Maven)
- Run the application: `mvn spring-boot:run` (Runs on port 8080)

### 3. Frontend (React)
- Navigate to `frontend/`
- Install dependencies: `npm install`
- Run in development mode: `npm run dev` (Runs on port 3000)

---

## 🛠 Features
- **Upload**: Supports PDF, DOCX, and TXT.
- **RAG**: Uses LangChain and ChromaDB for vector retrieval.
- **LLM**: Powered by GPT-4o-mini for accurate context-based answers.
- **Hallucination Protection**: Strictly answers from the uploaded context.

---

## 📂 Folder Structure
```
rag-app/
├── ai-service/     # FastAPI, ChromaDB, Document Processing
├── backend/        # Spring Boot Controllers & Services
└── frontend/       # React (Vite) + Vanilla CSS Glassmorphism
```
