#!/usr/bin/env python3
"""Verify embeddings and semantic search in Qdrant."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from qdrant_client import QdrantClient

from src.processing.embedder import TaxEmbedder


def verify_embeddings() -> None:
	"""Test semantic search with embeddings in Qdrant."""
	print("=" * 70)
	print("EMBEDDING VERIFICATION & SEMANTIC SEARCH TEST")
	print("=" * 70)

	# Initialize clients
	print("\n[1] Initializing Qdrant and TaxEmbedder...")
	client = QdrantClient(host="localhost", port=6333)
	embedder = TaxEmbedder()

	print(f"   Qdrant: localhost:6333")
	print(f"   Embedder: {embedder.model_name}")
	print(f"   Embedding dimension: {embedder.get_embedding_dim()}")

	# Check collection exists
	try:
		collection_info = client.get_collection("tax_code_raw")
		print(f"   Collection points: {collection_info.points_count}")
	except Exception as e:
		print(f"   Error: Collection not found. {e}")
		print("   Run parser first: python -m src.ingestion.parser")
		sys.exit(1)

	# Test query
	test_query = "How are dependents defined?"
	print(f"\n[2] Embedding test query: '{test_query}'")
	query_embedding = embedder.embed_text(test_query)
	print(f"   Vector generated: {len(query_embedding)} dimensions")

	# Search
	print("\n[3] Searching top 3 closest sections...")
	try:
		results = client.search(
			collection_name="tax_code_raw",
			query_vector=query_embedding,
			limit=3,
		)
	except Exception as e:
		print(f"   Error during search: {e}")
		sys.exit(1)

	if not results:
		print("   No results found.")
		sys.exit(1)

	# Print results
	print("\n[4] Results:")
	print("   " + "-" * 66)
	high_score_count = 0
	for i, point in enumerate(results, 1):
		section_number = point.payload.get("section_number", "Unknown")
		title = point.payload.get("title", "Untitled")
		score = point.score
		status = "✓" if score > 0.7 else "○"
		print(f"   {status} #{i}: {section_number}")
		print(f"      Title: {title}")
		print(f"      Similarity Score: {score:.4f}")
		if score > 0.7:
			high_score_count += 1

	print("   " + "-" * 66)

	# Summary
	print("\n[5] Summary:")
	if high_score_count >= 2:
		print("   ✓ Semantic search is operational!")
		print(f"   Found {high_score_count}/3 results with high similarity (> 0.7)")
	else:
		print("   ○ Semantic search active but scores are lower than expected.")
		print(f"   Found {high_score_count}/3 high-similarity results.")

	print("\n" + "=" * 70)


if __name__ == "__main__":
	verify_embeddings()
