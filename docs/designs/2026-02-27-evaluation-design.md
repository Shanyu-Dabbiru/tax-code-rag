# Phase 5 Evaluation Architecture Design

**Date:** 2026-02-27
**Topic:** RAG Evaluation CLI and Synthetic Dataset Generation

## Overview
Phase 5 focuses on building the "Evaluation" layer of the project. We will mathematically measure the performance of our Phase 4 Hybrid Search API (both its precision in retrieving the correct law, and the faithfulness of an LM answering based on that law). To do this repeatably without massive manual labor, we will construct an automated Python-based CI/CD-style evaluation script using the `ragas` framework.

## Architecture

### 1. Synthetic Dataset Generation (The "Ground Truth")
We will implement an automated offline script to generate our test dataset.
- **Source Data:** The script will query Qdrant (or read our `taxes.jsonl` file) to pull 50 random, complex tax sections (e.g., Section 162, Section 401k).
- **LLM Question Generation:** We will pass these sections to an LLM (e.g., GPT-4o-mini or Claude 3.5 Sonnet) via API with reading comprehension prompts to generate realistic user questions.
- **Output:** A static `.csv` or `.json` dataset containing pairs of `{"question": "Can I deduct...", "ground_truth_context": ["Section 162..."]}`.
- *Reasoning:* This leverages the LLM's reading comprehension to build a robust test suite in seconds without hallucinatory risks.

### 2. The Evaluation Pipeline
We will skip interactive Jupyter Notebooks in favor of a strict, repeatable Python CLI (`src/evaluation/run_evals.py`).
- **Input:** The script loads the synthetic `.csv` dataset.
- **Execution:** It iterates through each question and hits the actual Phase 4 FastAPI `/search` endpoint to get the Top 5 retrieved chunks.
- **Scoring (Ragas):** 
  - It uses an LLM-as-a-Judge (via the `ragas` library) to calculate the **Context Precision** (did the API return the *right* law in the top 5?).
  - It generates a final answer to the question using the retrieved chunks, and scores **Faithfulness** (did the final answer hallucinate beyond the provided text?).
- **Output:** The script will output a final report (e.g., `eval_results_timestamp.json`) and optionally log the run metrics to Arize Phoenix for visual tracking.

## Next Steps
With this design approved, we will transition to the **Planning skill** to generate the step-by-step implementation plan for writing the Synthetic Generator Script and the Ragas Evaluation CLI.
