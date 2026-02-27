from qdrant_client import QdrantClient
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wipe():
    qdrant = QdrantClient(url="http://localhost:6333")
    col_name = "tax_code_chunks"
    if qdrant.collection_exists(col_name):
        logger.info(f"Deleting collection {col_name}")
        qdrant.delete_collection(col_name)
    else:
        logger.info(f"Collection {col_name} does not exist.")

if __name__ == "__main__":
    wipe()
