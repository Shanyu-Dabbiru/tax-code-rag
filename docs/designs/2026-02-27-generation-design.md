# Phase 6 Generation Architecture Design

**Date:** 2026-02-27
**Topic:** RAG Generation API Endpoint (The "Two-Step" Approach)

## Overview
Phase 6 focuses on the "Generation" component of our Retrieval-Augmented Generation pipeline. We will implement an endpoint that takes retrieved tax code chunks and formats them using a Large Language Model (LLM) to produce a plain-English answer for the user. We will use the Two-Step approach (Option C) to ensure the frontend remains fast and the backend logic remains cleanly decoupled.

## Architecture

### 1. The Endpoints
We will maintain two separate, decoupled endpoints in the FastAPI application:
- **`POST /search` (Existing):** Takes a user query and returns the top 5 relevant chunks using Qdrant Hybrid Search + Cross-Encoder reranking.
- **`POST /generate` (New):** Takes the user query AND the exact text of the 5 retrieved chunks. It passes these to an LLM to generate the final response and returns it as a string.

### 2. Payload Design
**Request to `/generate`:**
```json
{
  "query": "Are moving expenses deductible?",
  "contexts": [
    {"chunk_id": "123", "text": "Section 217: Moving expenses are not deductible...", "score": 0.95}
  ]
}
```

**Response from `/generate`:**
```json
{
  "answer": "Under Section 217, moving expenses are not currently deductible for most taxpayers unless you are an active duty member of the Armed Forces..."
}
```

### 3. LLM Integration (Prompt Engineering)
We will use the OpenAI API (e.g., `gpt-4o` or `gpt-4o-mini`) via the `openai` Python SDK. We will construct a strict system prompt:
> "You are an expert CPA. Answer the user's question using strictly the provided Context chunks. Do not use outside knowledge. If the context does not answer the question, say 'The provided tax code does not have the answer'."

### 4. Client Interaction Flow (for Phase 7)
1. Frontend calls `/search` with the user's question.
2. Frontend instantly displays the top 5 source documents to the user (e.g., "Reading Section 162...").
3. Frontend immediately makes a second call to `/generate`, passing the context it just received.
4. Frontend displays a loading spinner for the answer, then displays it when it arrives a few seconds later.

## Next Steps
Transition to the **Planning skill** to write the step-by-step implementation plan for adding the `/generate` endpoint to the FastAPI application.
