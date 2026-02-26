# 4-Week Development Roadmap

- [x] **Phase 1: Infrastructure**: Deploy Qdrant and Arize Phoenix via Docker Compose.
- [ ] **Phase 2: Ingestion (Current)**: Build the `TaxParser` batch processor using `ProcessPoolExecutor` to extract and validate Title 26 HTML fragments.
- [ ] **Phase 3: Embedding & Storage**: Integrate `BAAI/bge-small-en-v1.5` (384 dimensions) via `sentence-transformers` and upsert to Qdrant.
- [ ] **Phase 4: Retrieval & API**: Build FastAPI backend with Hybrid Search (BM25 + Vector) and Cross-Encoder Reranking.
- [ ] **Phase 5: Evaluation**: Use Ragas framework to score Faithfulness and Context Precision.