# Phase 4 API Architecture Design

**Date:** 2026-02-26
**Topic:** FastAPI Retrieval Backend (Hybrid Search + Reranking)

## Overview
Phase 4 focuses on building the "T" (Translate & Retrieve) layer of the A.N.T structure. We will implement a robust FastAPI backend that takes a user query, translates it directly into mathematical concepts (Dense Embeddings) and keywords (Sparse/BM25 Vectors), hits Qdrant for a hybrid retrieval, and applies a local cross-encoder model to sort the retrieved chunks by true semantic relevance.

## Architecture

### 1. Endpoints
We will deploy a monolithic **`/search`** endpoint to keep the frontend contract simple. 
- **Input:** JSON payload with `query` (str) and optional `top_k` (int).
- **Processing:** The server will handle all the complex routing (Embedding → Hybrid Search → Reranking).
- **Output:** A JSON array of the top 5 `TaxSection` chunks, complete with their `enriched_text` and `hierarchy` metadata for easy LLM prompt injection downstream.

### 2. Retrieval Strategy: Qdrant Native Hybrid Search
We will leverage **Native Qdrant Sparse Vectors**.
- The existing Qdrant collection (`tax_code_chunks`) currently only holds dense vectors (384 dimensions from `BAAI/bge-small-en-v1.5`).
- We will update the ingestion/embedding pipeline to *also* generate sparse BM25 vectors using an efficient local model (like `Qdrant/bm25` or `prithivida/Splade_PP_en_v1`).
- During search, FastAPI will query Qdrant with *both* the dense query vector and sparse query vector. Qdrant natively fuses these (via Reciprocal Rank Fusion) and returns the top 20 candidate chunks.

### 3. Reranking Strategy: In-Memory Local Model
To maximize privacy and avoid API costs, we will use an **In-Memory Local Reranker**.
- We will integrate a Cross-Encoder model (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2` or `BAAI/bge-reranker-base`) directly into the FastAPI application state.
- The server will pass the user's string query alongside the top 20 chunks retrieved from Qdrant through the reranker.
- The top 5 chunks with the highest reranker scores will be returned to the client.

## Next Steps
With this design approved, we will transition to the **Planning skill** to generate the exact implementation plan (creating the FastAPI skeleton, updating the chunking script for sparse vectors, and wiring the reranker).
