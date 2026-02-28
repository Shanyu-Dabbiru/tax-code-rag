# Phase 7 Frontend Architecture Design

**Date:** 2026-02-27
**Topic:** Tax Code RAG Chat Interface (Next.js)

## Overview
Phase 7 focuses on building the User Interface for our Tax Code RAG pipeline. We will use a modern React framework (Next.js) to build a beautiful, pixel-perfect frontend that strictly adheres to the "Origin Financial" brand guidelines defined in `design_guidelines/brand_guidelines.md`.

## Architecture & Framework

### 1. Technology Stack
- **Framework:** Next.js (App Router format for modern React server/client components).
- **Language:** TypeScript (for strict typing of our Search and Generate API payloads).
- **Styling:** Tailwind CSS (configured to exactly match the JSON brand guidelines) or pure CSS Modules depending on execution preference, but Tailwind allows for rapid replication of the design system.
- **Icons:** Lucide-React (clean, modern icons).

### 2. Design System Integration
The app will faithfully recreate the JSON guidelines:
- **Typography:** `Inter` font stack for all headers and body text.
- **Colors:**
  - Background: `#F9F9F7` (warm off-white)
  - Text: `#01000A` (near black)
  - Primary Action / Links: `#FA8072` (salmon/coral)
  - Accent: `#FAA2A1`
- **Components:**
  - Inputs (Search bar): 0px border radius, transparent background.
  - Primary Buttons: 8px border radius, `#01000A` background, `#FFFFFF` text.
  - Secondary/Action Buttons: 8px border radius, `#FFFFFF` background, `#7D7D81` border.

### 3. Application Layout & Interaction Flow
The interface will be a Chat/Search execution screen (as referenced by `Tax code rag chat interface.png`).

1. **The Hero State:** A clean, centered search bar requesting the user to ask a tax question.
2. **Step 1: The Retrieval State (Instant):** When the user searches, a `POST /search` request is sent to the FastAPI backend. The UI instantly populates with the 5 retrieved source chunks, displayed as interactive "Citation Cards".
3. **Step 2: The Generation State (Loading):** While the chunks are displayed, the UI shows a sleek loading indicator (e.g., "Thinking...") while a `POST /generate` request is made in the background to the FastAPI backend.
4. **Step 3: The Response State:** The final LLM answer replaces the loading indicator, formatted in clean Markdown.

### 4. Project Structure (Proposed)
The Next.js app will live in a separate directory at the root of the project to cleanly separate frontend from backend:
```
tax-code-rag/
├── src/ (FastAPI Backend)
├── data/
└── frontend/ (New Next.js App)
    ├── app/ (Routing)
    ├── components/ (UI Elements like CitationCard, ChatInput)
    ├── lib/ (API fetching logic)
    └── tailwind.config.ts (Brand colors/fonts)
```

## Next Steps
Once Phase 6 (Generation Layer) implementation is fully complete, we will use the **Planning skill** to write the step-by-step implementation plan for creating the Next.js scaffold, writing the components, and wiring up the API calls.
