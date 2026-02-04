"""
Pydantic models for tax code data structures.

This module defines the core data models used throughout the RAG pipeline
for validating, storing, and retrieving tax code information.
"""

from typing import Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field


class TaxSection(BaseModel):
    """
    Represents a single section of the Internal Revenue Code (Title 26, U.S.C.).

    This model encapsulates a tax law section with its hierarchical context,
    enabling Context-Aware Retrieval in the RAG pipeline. The hierarchy field
    preserves the statutory path (Title > Subtitle > Chapter > Section), which
    is critical for:

    1. **Semantic Context**: When retrieving Section 162 (business deductions),
       the hierarchy helps the LLM understand it's nested under Chapter 1
       (Normal Taxes and Surtaxes). This prevents mixing unrelated sections.

    2. **Cross-Reference Navigation**: Tax law is highly interconnected. The
       hierarchy enables the retrieval system to recommend related sections
       (e.g., Section 162 → Section 163 → Section 164) by traversing the
       same parent nodes.

    3. **Chunk Granularity**: During RAG embedding, we can use hierarchy to
       group related subsections, improving retrieval precision over naive
       text chunking.

    4. **Ranking Signals**: In hybrid retrieval (BM25 + vector search), hierarchy
       can boost exact-match scores when user queries mention a known chapter
       or title.

    Example:
        A section on business deductions might have:
        - section_number: "26 U.S.C. § 162"
        - title: "Trade or business expenses"
        - hierarchy: ["Title 26", "Subtitle A", "Chapter 1", "Section 162"]

    This structure ensures the retrieval pipeline returns not just textual
    matches, but semantically coherent sections grounded in tax law structure.
    """

    id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for database indexing and deduplication."
    )

    section_number: str = Field(
        ...,
        description="Canonical section number (e.g., '26 U.S.C. § 162'). "
                    "Used for exact lookup and citation matching."
    )

    title: str = Field(
        ...,
        description="Human-readable title/name of the section "
                    "(e.g., 'Trade or business expenses')."
    )

    content: str = Field(
        ...,
        description="Full text of the tax section. Stored verbatim from source; "
                    "cleaning (boilerplate removal) happens at parser level."
    )

    hierarchy: List[str] = Field(
        ...,
        description="Hierarchical path from root to this section. "
                    "Example: ['Title 26', 'Subtitle A', 'Chapter 1', 'Section 162']. "
                    "Enables context-aware retrieval and cross-reference navigation."
    )

    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Flexible key-value store for auxiliary information. "
                    "Examples: 'effective_date', 'source_url', 'amendment_history', 'version'."
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when this record was created/ingested."
    )

    class Config:
        """Pydantic v2 configuration."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "section_number": "26 U.S.C. § 162",
                "title": "Trade or business expenses",
                "content": "(a) In general. There shall be allowed as a deduction "
                          "all the ordinary and necessary expenses paid or incurred "
                          "during the taxable year in carrying on any trade or business...",
                "hierarchy": ["Title 26", "Subtitle A", "Chapter 1", "Subchapter B", "Section 162"],
                "metadata": {
                    "effective_date": "1954-01-01",
                    "source_url": "https://www.irs.gov/publications/irs-pdf/p17.pdf",
                    "version": "2024-01"
                },
                "created_at": "2024-01-15T10:30:00"
            }
        }
