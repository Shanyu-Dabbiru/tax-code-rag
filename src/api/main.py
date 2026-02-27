import logging
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.api.retriever import HybridRetriever, ChunkResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tax RAG API",
    description="API for searching the Tax Code using Hybrid Search",
    version="0.1.0"
)

# Request/Response Models
class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of top results to return")

class SearchResponse(BaseModel):
    results: List[ChunkResponse]

# Global retriever instance
retriever: HybridRetriever = None

@app.on_event("startup")
def startup_event():
    global retriever
    logger.info("Initializing HybridRetriever...")
    retriever = HybridRetriever()
    logger.info("HybridRetriever initialized.")

@app.post("/search", response_model=SearchResponse)
def search_endpoint(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        chunks = retriever.search(query=request.query, top_k=request.top_k)
        # Note: the retriever currently returns 20 pre-reranked chunks regardless of top_k (Task 2 spec).
        # Task 3 will apply the reranker and slice top_k.
        return SearchResponse(results=chunks)
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))
