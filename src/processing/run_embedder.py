import argparse
import json
import logging
import sys
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams, Distance

from src.processing.chunker import chunk_text
from src.processing.embedder import TaxEmbedder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Embed and upsert tax code chunks to Qdrant")
    parser.add_argument("--input", required=True, help="Path to input jsonl file")
    parser.add_argument("--qdrant-url", default=os.getenv("QDRANT_URL", "http://localhost:6333"), help="Qdrant URL")
    parser.add_argument("--collection", default="tax_code_chunks", help="Collection name")
    parser.add_argument("--batch-size", default=64, type=int, help="Batch size for embedding and upsert")
    return parser.parse_args()

def init_collection(qdrant: QdrantClient, collection_name: str, vector_size: int):
    try:
        collections = qdrant.get_collections().collections
        exists = any(c.name == collection_name for c in collections)
        if not exists:
            logger.info(f"Creating collection '{collection_name}' with size {vector_size} (dense + sparse)")
            qdrant.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "dense": models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
                },
                sparse_vectors_config={
                    "sparse": models.SparseVectorParams()
                }
            )
        else:
            logger.info(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        logger.error(f"Failed to check/create collection: {e}")
        sys.exit(1)

def main():
    args = parse_args()
    
    logger.info("Initializing Qdrant client and embedder...")
    qdrant = QdrantClient(url=args.qdrant_url, api_key=os.getenv("QDRANT_API_KEY"))
    embedder = TaxEmbedder()
    vector_size = embedder.get_embedding_dim()
    
    init_collection(qdrant, args.collection, vector_size)
    
    points_data = []
    
    logger.info(f"Reading from {args.input}")
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            
            section_id = data.get("id")
            if not section_id:
                section_id = str(uuid.uuid4())
                
            title = data.get("title", "")
            content = data.get("content", "")
            hierarchy = data.get("hierarchy", [])
            path = " > ".join(hierarchy)
            
            # Reconstruct the enriched text
            enriched_text = f"{path}\n{title}\n{content}".strip()
            
            # Chunk the content
            chunks = chunk_text(enriched_text, max_chars=1500)
            
            for i, chunk in enumerate(chunks):
                # Scoped UUID5 based on original section ID + chunk index
                chunk_id_str = str(uuid.uuid5(uuid.UUID(section_id), str(i)))
                
                payload = {
                    "parent_id": section_id,
                    "chunk_index": i,
                    "text": chunk,
                    "title": title,
                    "hierarchy": hierarchy,
                    "section_number": data.get("section_number", "")
                }
                
                points_data.append((chunk_id_str, payload, chunk))
                
    logger.info(f"Total chunks to embed and upsert: {len(points_data)}")
    
    for i in range(0, len(points_data), args.batch_size):
        batch = points_data[i:i + args.batch_size]
        texts = [b[2] for b in batch]
        
        logger.info(f"Embedding dense and sparse batch {i} to {min(i + args.batch_size, len(points_data))}...")
        dense_embeddings = embedder.embed_batch(texts)
        sparse_embeddings = embedder.embed_sparse_batch(texts)
        
        qdrant_points = []
        for j, (chunk_id_str, payload, text) in enumerate(batch):
            qdrant_points.append(
                PointStruct(
                    id=chunk_id_str,
                    vector={
                        "dense": dense_embeddings[j],
                        "sparse": models.SparseVector(
                            indices=sparse_embeddings[j]["indices"],
                            values=sparse_embeddings[j]["values"]
                        )
                    },
                    payload=payload
                )
            )
            
        logger.info(f"Upserting batch {i} to {min(i + args.batch_size, len(points_data))}...")
        qdrant.upsert(
            collection_name=args.collection,
            points=qdrant_points
        )

    logger.info("Done!")

if __name__ == "__main__":
    main()
