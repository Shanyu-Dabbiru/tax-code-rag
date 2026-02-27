# Pipeline Ingestion & Embedding Design

**Date:** 2026-02-26
**Topic:** End-to-End Parsing and Embedding Pipeline

## Overview
Currently, the ingestion pipeline parses HTML files and directly upserts them to Qdrant in a single memory-bound process. This design document outlines the agreed-upon architecture to decouple parsing from embedding, enhance search relevance through enriched text payloads, and handle long statutes via chunking.

## Architecture & Data Flow

### 1. Decoupled Pipeline (Persisted JSONL)
- **Parser Step (`run_parser.py`)**: The `TaxParser` will no longer connect to Qdrant or initialize the `TaxEmbedder`. It will strictly read HTML, validate `TaxSection` objects, and write them sequentially to `data/processed/taxes.jsonl`.
- **Embedder Step (`run_embedder.py`)**: A new independent script will stream lines from `taxes.jsonl`, chunk the text, generate embeddings via `BAAI/bge-small-en-v1.5`, and upsert to Qdrant.
- **Advantage**: If Qdrant rate limits or the embedding model crashes, we do not lose the parsing progress.

### 2. Enriched Content Chunking
- **Text Payload**: We will not embed raw content. Instead, we will construct an enriched string:
  `[Hierarchy Path] \n [Title] \n [Content Chunk]`
- **Chunking Strategy**: Because Title 26 sections can be exceptionally long (exceeding the 512 token limit of bge-small), we will split the `content` into chunks. 
- **Qdrant Storage**: Each chunk will be upserted as a separate point/vector in Qdrant. The payload for each point will contain its specific text chunk, alongside the `parent_id` (the UUID of the base `TaxSection`) and the full metadata (hierarchy, effective date, etc.), allowing us to trace any matched chunk back to its source section.

## Next Steps
With this design approved, we will transition to the **Planning** skill to write the exact implementation plan (file paths, classes to modify, and tests to run) to fulfill this architecture.
