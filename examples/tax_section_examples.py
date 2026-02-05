"""
Example instances of TaxSection demonstrating the enhanced MVP schema.

These examples show how the model handles:
1. Simple rule (§ 162 - business expenses)
2. Complex rule with exceptions (§ 179 - election to expense depreciable assets)
3. Multi-subsection comprehensive section (§ 61 - gross income defined)
"""

import sys
from pathlib import Path
from datetime import datetime
from uuid import UUID

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.tax_data import TaxSection, SectionType


# Example 1: Simple section with straightforward rule
section_162 = TaxSection(
    id=UUID("550e8400-e29b-41d4-a716-446655440000"),
    parent_id=None,  # Top-level section under Subchapter B
    section_number="26 U.S.C. § 162",
    title="Trade or business expenses",
    content="""(a) In general. There shall be allowed as a deduction all the ordinary 
and necessary expenses paid or incurred during the taxable year in carrying on any 
trade or business, including—
(1) a reasonable allowance for salaries or other compensation for personal services 
actually rendered;
(2) traveling expenses (including amounts expended for meals and lodging other than 
amounts which are lavish or extravagant under the circumstances) while away from 
home in the pursuit of a trade or business; and
(3) rentals or other payments required to be made as a condition to the continued 
use or possession, for purposes of the trade or business, of property to which the 
taxpayer has not taken or is not taking title or in which he has no equity.""",
    hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Subchapter B", "Part VI", "Section 162"],
    section_type=SectionType.SECTION,
    subsections=["(a) In general"],
    effective_date=datetime(1954, 1, 1),
    source_url="https://www.law.cornell.edu/uscode/text/26/162",
    metadata={
        "version": "2024-01",
        "last_amended": "1986-10-22",
        "related_sections": "§ 163, § 164, § 165"  # Defer to TaxCrossReference post-MVP
    },
    created_at=datetime(2024, 1, 15, 10, 30)
)


# Example 2: Complex section with phase-outs, exceptions, and dollar limits
section_179 = TaxSection(
    id=UUID("660e8400-e29b-41d4-a716-446655440001"),
    parent_id=None,
    section_number="26 U.S.C. § 179",
    title="Election to expense certain depreciable business assets",
    content="""(a) Treatment as expenses. A taxpayer may elect to treat the cost of any 
section 179 property as an expense which is not chargeable to capital account. Any cost 
so treated shall be allowed as a deduction for the taxable year in which the section 179 
property is placed in service.

(b) Limitations.
(1) Dollar limitation. The aggregate cost which may be taken into account under 
subsection (a) for any taxable year shall not exceed $1,160,000.
(2) Reduction in limitation. The limitation under paragraph (1) shall be reduced 
(but not below zero) by the amount by which the cost of section 179 property placed 
in service during the taxable year exceeds $2,890,000.

(c) Election.
(1) In general. An election under this section for any taxable year shall—
(A) specify the items of section 179 property to which the election applies and 
the portion of the cost of each of such items which is to be taken into account 
under subsection (a), and
(B) be made on the taxpayer's return of the tax imposed by this chapter for the 
taxable year.

(d) Definitions and special rules.
(1) Section 179 property. For purposes of this section, the term "section 179 property" 
means property which is—
(A) tangible property (to which section 168 applies),
(B) acquired by purchase for use in the active conduct of a trade or business, and
(C) not described in the last sentence of section 168(f)(1).""",
    hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Subchapter B", "Part VI", "Section 179"],
    section_type=SectionType.SECTION,
    subsections=[
        "(a) Treatment as expenses",
        "(b) Limitations",
        "(c) Election",
        "(d) Definitions and special rules"
    ],
    effective_date=datetime(1958, 1, 1),
    source_url="https://www.law.cornell.edu/uscode/text/26/179",
    metadata={
        "version": "2024-01",
        "last_amended": "2023-12-29",  # Inflation adjustments
        "dollar_limit_2024": "1160000",
        "phase_out_threshold_2024": "2890000",
        "inflation_adjusted": "true",
        "sunset_date": "None",  # Permanent provision
        # Post-MVP: Move to ApplicabilityScope model
        "applies_to": "businesses,individuals,partnerships,corporations"
    },
    created_at=datetime(2024, 1, 15, 10, 35)
)


# Example 3: Multi-subsection comprehensive section (foundation of income tax)
section_61 = TaxSection(
    id=UUID("770e8400-e29b-41d4-a716-446655440002"),
    parent_id=None,
    section_number="26 U.S.C. § 61",
    title="Gross income defined",
    content="""(a) General definition. Except as otherwise provided in this subtitle, 
gross income means all income from whatever source derived, including (but not limited to) 
the following items:
(1) Compensation for services, including fees, commissions, fringe benefits, and similar items;
(2) Gross income derived from business;
(3) Gains derived from dealings in property;
(4) Interest;
(5) Rents;
(6) Royalties;
(7) Dividends;
(8) Annuities;
(9) Income from life insurance and endowment contracts;
(10) Pensions;
(11) Income from discharge of indebtedness;
(12) Distributive share of partnership gross income;
(13) Income in respect of a decedent; and
(14) Income from an interest in an estate or trust.""",
    hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Subchapter B", "Part I", "Section 61"],
    section_type=SectionType.SECTION,
    subsections=[
        "(a) General definition",
        "(1) Compensation for services",
        "(2) Gross income derived from business",
        "(3) Gains derived from dealings in property",
        "(4) Interest",
        "(5) Rents",
        "(6) Royalties",
        "(7) Dividends",
        "(8) Annuities",
        "(9) Income from life insurance and endowment contracts",
        "(10) Pensions",
        "(11) Income from discharge of indebtedness",
        "(12) Distributive share of partnership gross income",
        "(13) Income in respect of a decedent",
        "(14) Income from an interest in an estate or trust"
    ],
    effective_date=datetime(1954, 1, 1),
    source_url="https://www.law.cornell.edu/uscode/text/26/61",
    metadata={
        "version": "2024-01",
        "last_amended": "1996-08-20",
        "foundational_section": "true",
        "treasury_reg": "26 CFR § 1.61-1",  # Post-MVP: Move to RegulatoryReference model
        # Post-MVP: Extract to DefinitionSet model
        "defines": "gross income,compensation,dividends,interest,rents,royalties"
    },
    created_at=datetime(2024, 1, 15, 10, 40)
)


# Example 4: Subsection (child of § 162) demonstrating parent_id usage
subsection_162a = TaxSection(
    id=UUID("880e8400-e29b-41d4-a716-446655440003"),
    parent_id=UUID("550e8400-e29b-41d4-a716-446655440000"),  # Links to § 162
    section_number="26 U.S.C. § 162(a)",
    title="Trade or business expenses - In general",
    content="""There shall be allowed as a deduction all the ordinary and necessary 
expenses paid or incurred during the taxable year in carrying on any trade or business, 
including—
(1) a reasonable allowance for salaries or other compensation for personal services 
actually rendered;
(2) traveling expenses (including amounts expended for meals and lodging other than 
amounts which are lavish or extravagant under the circumstances) while away from 
home in the pursuit of a trade or business; and
(3) rentals or other payments required to be made as a condition to the continued 
use or possession, for purposes of the trade or business, of property to which the 
taxpayer has not taken or is not taking title or in which he has no equity.""",
    hierarchy=[
        "Title 26", 
        "Subtitle A", 
        "Chapter 1", 
        "Subchapter B", 
        "Part VI", 
        "Section 162",
        "Subsection (a)"
    ],
    section_type=SectionType.SUBSECTION,  # Not a full section—fragment for granular retrieval
    subsections=["(1) Salaries", "(2) Travel expenses", "(3) Rentals"],
    effective_date=datetime(1954, 1, 1),
    source_url="https://www.law.cornell.edu/uscode/text/26/162#a",
    metadata={
        "version": "2024-01",
        "parent_section": "§ 162",
        "ordinarily_necessary_test": "true"  # Key doctrinal standard
    },
    created_at=datetime(2024, 1, 15, 10, 45)
)


if __name__ == "__main__":
    """Demonstrate schema validation and usage."""
    
    # Validate that all examples pass Pydantic validation
    examples = [section_162, section_179, section_61, subsection_162a]
    
    for example in examples:
        print(f"\n{'='*80}")
        print(f"Section: {example.section_number}")
        print(f"Type: {example.section_type.value}")
        print(f"Parent ID: {example.parent_id}")
        print(f"Title: {example.title}")
        print(f"Hierarchy depth: {len(example.hierarchy)} levels")
        print(f"Subsections: {len(example.subsections)} found")
        print(f"Effective date: {example.effective_date}")
        print(f"Content length: {len(example.content)} chars")
        print(f"Metadata keys: {', '.join(example.metadata.keys())}")
    
    print(f"\n{'='*80}")
    print("✓ All examples validated successfully against TaxSection schema")
    print(f"✓ Total examples: {len(examples)}")
    print("\nKey schema improvements:")
    print("1. parent_id enables tree queries: e.g., 'find all children of § 162'")
    print("2. section_type enables ranking: prefer 'section' over 'subsection' in results")
    print("3. subsections enables snippet preview without re-parsing content")
    print("4. effective_date enables temporal queries: 'retrieve § 179 as of 2023-01-01'")
    print("5. source_url provides data lineage tracking")
