# tax-code-pipeline 🏛️
A production-ready RAG pipeline for indexing and querying Title 26 (Internal Revenue Code). This project focuses on the engineering challenges of handling hierarchical legal structures, metadata integrity, and system observability.

🏗 System Architecture
- ETL & Ingestion: Custom Python-based parser for Title 26 XML. Implements cleaning logic to strip boilerplate while preserving statutory hierarchy.
- Hierarchical Indexing: Moves beyond fixed-length windowing to semantic section-based chunking, ensuring retrieval preserves legal context.
- Vector Store: Qdrant (Dockerized) for metadata-filtered vector search.
- Observability: Arize Phoenix (OpenTelemetry) integration for trace logging, latency tracking, and retrieval debugging.
- Evaluation: Quantitative benchmarking via Ragas (Faithfulness, Relevancy, and Context Precision).

🛠 Tech Stack
- Python 3.10+
- Infrastructure: Docker, Docker Compose
- Vector DB: Qdrant
- Observability: Arize Phoenix / OpenTelemetry
- Orchestration: LlamaIndex (or LangChain)

📂 Repository Structure
.
├── src/
│   ├── ingestion/    # XML/HTML parsing & cleaning
│   ├── processing/   # Hierarchical chunking & embedding
│   ├── retrieval/    # Hybrid search & reranking logic
│   └── api/          # FastAPI entry points
├── infra/            # Docker Compose & DB configs
├── eval/             # Ragas evaluation scripts
└── data/             # Raw Title 26 sources (git-ignored)
