"""
Olasquare Bot(RAG System) with API 

Provides endpoint to query Olasquare Bot (RAG System)
"""

from helper import DocumentProcessing, VectorManager, RagBuilder
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
# import uvicorn
import asyncio

# Query models
class QueryRequest(BaseModel):
    question: str =Field(..., example="Who is Ola?")

class QueryResponse(BaseModel):
    question:str 
    answer: str

class VectorSearchRequest(BaseModel):
    query: str = Field(..., example="How old is Olasquare?")
    results: list

# global variables
vector_manager: VectorManager|None= None
doc_processing:DocumentProcessing|None= None
rag_builder: RagBuilder|None= None
vector_store= None
@asynccontextmanager
async def lifespan(app:FastAPI):
    global vector_manager, doc_processing, rag_builder,vector_store
    print("🔃 Loading RAG system...")
    vector_manager=VectorManager()
    doc_processing=DocumentProcessing()
    rag_builder=RagBuilder(vector_manager)
    vector_store =vector_manager.load_vectorstore()
    print("✅ RAG system loaded!")
    yield

     # Shutdown: release any held resources if needed
    print("Shutting down RAG system...")
    vector_store = None
    rag_builder = None
    doc_processing=None
    vector_manager=None

# Initialize FastAPI app
app= FastAPI(lifespan=lifespan, title="Olasqaure Personal Bot", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Olasquare Personal Bot is running"}

@app.get("/health")
async def healthcheck():
    if not rag_builder:
        raise RuntimeError ("Olasquare Personal Bot (RAG system) is unavailable")
    return {"status":"ok"}

@app.post ("/chat", response_model= QueryResponse)
async def ask (chat_request:QueryRequest):
    if not rag_builder:
        raise RuntimeError ("Olasquare Personal Bot (RAG system) is not ready")
    try:
        loop= asyncio.get_running_loop()
        print(">>> Calling LLM now")
        result= await loop.run_in_executor(None,rag_builder.query, chat_request.question)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException (status_code=500,detail={"message":"Ooops! something wrong", "error":str(e)})
