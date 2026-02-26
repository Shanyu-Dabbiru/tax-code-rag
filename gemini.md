# Tax Intelligence RAG Pipeline - Constitution

## 1. Architectural Invariants
- **Language**: Python 3.10+
- **Data Validation**: Strictly use Pydantic (V2) for all data models.
- **Parsing**: Use `lxml` and Regex for high-performance HTML/XML parsing.
- **Observability**: Use OpenTelemetry (`opentelemetry-sdk`) to route all traces and validation errors to Arize Phoenix (Port 4317).
- **Vector Database**: Qdrant (Dockerized on Port 6333) using cosine similarity.
- **Architecture**: A modular, 3-layer A.N.T structure.

## 2. Behavioral Rules
- **Self-Annealing**: Do not silently ignore errors. Log validation failures to Phoenix as events, fail fast, and skip bad files without crashing the batch.
- **Modularity**: Separation of ETL (Ingestion), Indexing, and Retrieval.

## 3. Data Schema (The "Payload")
All ingested HTML files must map to this Pydantic `TaxSection` schema before hitting Qdrant:
- `id`: UUID
- `section_number`: str (e.g., "26 U.S.C. § 162")
- `title`: str
- `content`: str (Cleaned statute text)
- `hierarchy`: List[str] (e.g., ["Title 26", "Subtitle A", "Chapter 1"])
- `section_type`: Enum (Title, Subtitle, Chapter, Section, etc.)
- `subsections`: List[str]
- `effective_date`: datetime
- `source_url`: Optional[str]
- `metadata`: Dict (contains `documentid`, `usckey`, `itempath`)