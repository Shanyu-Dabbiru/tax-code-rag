import logging
from typing import List, Dict, Any

from pydantic import BaseModel
from qdrant_client import QdrantClient, models

from src.processing.embedder import TaxEmbedder

logger = logging.getLogger(__name__)

class ChunkResponse(BaseModel):
    chunk_id: str
    text: str
    title: str
    hierarchy: List[str]
    section_number: str
    score: float

class HybridRetriever:
    def __init__(self, qdrant_url: str = "http://localhost:6333", collection_name: str = "tax_code_chunks"):
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.qdrant = QdrantClient(url=self.qdrant_url)
        self.embedder = TaxEmbedder()
        
    def search(self, query: str, top_k: int = 5) -> List[ChunkResponse]:
        """Perform a hybrid search using dense and sparse vectors via Qdrant Prefetch."""
        logger.info(f"Embedding query: '{query}'")
        
        dense_vector = self.embedder.embed_text(query)
        sparse_batch = self.embedder.embed_sparse_batch([query])
        sparse_vector = sparse_batch[0]
        
        logger.info(f"Querying Qdrant collection '{self.collection_name}' with Native Hybrid Search")
        
        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            prefetch=[
                models.Prefetch(
                    query=dense_vector,
                    using="dense",
                    limit=20
                ),
                models.Prefetch(
                    query=models.SparseVector(
                        indices=sparse_vector["indices"],
                        values=sparse_vector["values"]
                    ),
                    using="sparse",
                    limit=20
                )
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=20  # Return top 20 pre-reranked chunks as per plan
        )
        
        response_chunks = []
        for point in results.points:
            payload = point.payload or {}
            response_chunks.append(
                ChunkResponse(
                    chunk_id=str(point.id),
                    text=payload.get("text", ""),
                    title=payload.get("title", ""),
                    hierarchy=payload.get("hierarchy", []),
                    section_number=payload.get("section_number", ""),
                    score=point.score
                )
            )
            
        # Usually we would just return top_k, but the plan step 2 says:
        # 'Return the top 20 pre-reranked chunks.'
        # so we just return all 20 for now. Task 3 will handle the top_k cut.
        return response_chunks
