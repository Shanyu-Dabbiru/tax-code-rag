"""
Pydantic models for tax code data structures.

This module defines the core data models used throughout the RAG pipeline
for validating, storing, and retrieving tax code information.
"""

from typing import Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SectionType(str, Enum):
    """Hierarchical level of a tax code entry."""
    TITLE = "title"
    SUBTITLE = "subtitle"
    CHAPTER = "chapter"
    SUBCHAPTER = "subchapter"
    PART = "part"
    SECTION = "section"
    SUBSECTION = "subsection"
    PARAGRAPH = "paragraph"
    SUBPARAGRAPH = "subparagraph"


class TaxSection(BaseModel):
    """
    Represents a single section of the Internal Revenue Code (Title 26, U.S.C.).

    This model encapsulates a tax law section with its hierarchical context,
    enabling Context-Aware Retrieval in the RAG pipeline.
    
    **MVP Design Philosophy**: 
    This schema balances shipping speed with future-proofing. Four strategic fields 
    were added beyond the original design to prevent painful refactoring:
    
    1. `parent_id`: Enables tree queries without parsing hierarchy strings
    2. `section_type`: Allows ranking full sections higher than fragments  
    3. `subsections`: Captures structure during parsing for snippet preview
    4. `effective_date` + `source_url`: Type-safe fields vs. untyped metadata Dict
    
    **Deferred to Post-MVP** (add when needed, not blocking launch):
    - Cross-reference tracking (store in separate TaxCrossReference table)
    - Amendment history (add TaxAmendment model when temporal queries are required)
    - Structured content parsing (conditions/exceptions—defer until accuracy issues surface)
    - Applicability scoping (tax_years, affected_entities—add when filtering by entity type)
    
    The hierarchy field preserves the statutory path (Title > Subtitle > Chapter > Section), 
    which is critical for:

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

    parent_id: Optional[UUID] = Field(
        default=None,
        description="Foreign key to parent section for tree navigation. "
                    "Null for root nodes (Titles). Enables efficient queries like "
                    "'retrieve all subsections under § 162' without string parsing."
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

    section_type: SectionType = Field(
        default=SectionType.SECTION,
        description="Hierarchical level classification. Enables filtering by granularity "
                    "(e.g., rank full sections higher than paragraphs in search results)."
    )

    subsections: List[str] = Field(
        default_factory=list,
        description="Extracted subsection identifiers for quick parsing and preview. "
                    "Example: ['(a) In general', '(b) Charitable contributions', '(c) Rentals']. "
                    "Enables snippet generation without re-parsing full content."
    )

    effective_date: Optional[datetime] = Field(
        default=None,
        description="Date when this section/amendment became effective. "
                    "Enables temporal filtering ('retrieve § 179 as of 2023-01-01')."
    )

    source_url: Optional[str] = Field(
        default=None,
        description="Canonical source URL for this section (e.g., irs.gov, law.cornell.edu). "
                    "Used for citation verification and data lineage tracking."
    )

    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Flexible key-value store for additional fields not yet promoted to typed. "
                    "Examples: 'version', 'amendment_summary', 'repeal_date'. "
                    "Use sparingly—prefer typed fields for data used in retrieval filters."
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
                "parent_id": None,  # Root section has no parent
                "section_number": "26 U.S.C. § 162",
                "title": "Trade or business expenses",
                "content": "(a) In general. There shall be allowed as a deduction "
                          "all the ordinary and necessary expenses paid or incurred "
                          "during the taxable year in carrying on any trade or business...",
                "hierarchy": ["Title 26", "Subtitle A", "Chapter 1", "Subchapter B", "Section 162"],
                "section_type": "section",
                "subsections": ["(a) In general", "(b) Charitable contributions", "(c) Rentals or leases"],
                "effective_date": "1954-01-01T00:00:00Z",
                "source_url": "https://www.law.cornell.edu/uscode/text/26/162",
                "metadata": {
                    "version": "2024-01",
                    "last_amended": "1986-10-22"
                },
                "created_at": "2024-01-15T10:30:00"
            }
        }
