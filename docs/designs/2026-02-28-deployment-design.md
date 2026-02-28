# Phase 8 & Phase 9: Deployment and Observability Design

## Overview
This document outlines the architecture and hosting strategy to take the Tax Code RAG pipeline from a local development environment to a public, production-ready internet application. It also defines the strategy for monitoring the LLM's performance and token usage in real-time.

## Architecture Decisions

### 1. Frontend Hosting: Vercel
- **Why:** The frontend is a Next.js React application using the App Router. Vercel (the creator of Next.js) provides zero-configuration, instant global edge CDN hosting out of the box when connected to a GitHub repository.
- **How:** The `frontend` folder will be connected to a Vercel deployment pipeline. Production environment variables (`NEXT_PUBLIC_API_URL`) will be configured to point to the live backend URL.

### 2. Backend Hosting: Render
- **Why:** The backend is a Python FastAPI service exposing the `/search` and `/generate` endpoints. Render offers a generous Free Tier for Web Services. It easily handles Python dependencies (`requirements.txt`), FastAPI web servers (via `uvicorn`), and securely manages environment variables (OpenAI keys).
- **How:** The repository root will be connected to Render. The build command will be `pip install -r requirements.txt`, and the start command will be `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`.

### 3. Vector Database: Qdrant Cloud
- **Why:** Currently, the tax chunk embeddings live in a local Docker container. To make the backend stateless and publicly accessible, the vector store must also be in the cloud. Qdrant provides a fully managed SaaS "Free Cluster" (1GB limit), which is vastly more than enough for the 56 United States Tax Code chunks.
- **How:** A cluster will be provisioned at `cloud.qdrant.io`. An API key and Cluster URL will be generated. The `src/processing/run_embedder.py` script will be run one final time locally to upload the vectorized tax code to the cloud cluster.

### 4. Observability and Tracing: Arize Phoenix Cloud
- **Why:** The project currently has `opentelemetry-sdk` installed, but the telemetry data is not being captured. To monitor LLM hallucinations, retrieval context precision, and OpenAI token costs in production, a remote dashboard is needed. Arize Phoenix Cloud provides a managed SaaS dashboard that accepts OpenTelemetry data.
- **How:** The FastAPI backend will update its OpenTelemetry exporter configuration to point to `https://app.phoenix.arize.com:4317` using an Arize Phoenix Cloud API key.

## Data Flow
1. User visits the Vercel-hosted URL.
2. The user submits a query. The Vercel app makes an HTTP POST request to the Render-hosted FastAPI `/search` endpoint.
3. The Render app queries the Qdrant Cloud cluster and returns the chunks.
4. The Vercel app makes an HTTP POST request to the Render-hosted FastAPI `/generate` endpoint.
5. The Render app calls the OpenAI API to generate a response. Simultaneously, the OpenTelemetry instrumentor asynchronously sends the trace (latency, tokens, prompt text) to Arize Phoenix Cloud.
6. The Render app returns the synthesized response to Vercel, completing the UI flow.
