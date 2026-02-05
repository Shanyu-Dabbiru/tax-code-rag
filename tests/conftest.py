"""
Pytest configuration and shared fixtures for the test suite.

This module provides reusable fixtures that can be used across all test files.
"""

from datetime import datetime
from uuid import uuid4

import pytest

from src.models.tax_data import TaxSection, SectionType


@pytest.fixture
def sample_tax_section():
    """
    Fixture providing a basic TaxSection instance for testing.
    """
    return TaxSection(
        section_number="26 U.S.C. § 162",
        title="Trade or business expenses",
        content=(
            "(a) In general. There shall be allowed as a deduction all the ordinary "
            "and necessary expenses paid or incurred during the taxable year in "
            "carrying on any trade or business..."
        ),
        hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Subchapter B", "Section 162"],
    )


@pytest.fixture
def sample_tax_section_with_subsections():
    """
    Fixture providing a TaxSection with subsections.
    """
    return TaxSection(
        section_number="26 U.S.C. § 162",
        title="Trade or business expenses",
        content=(
            "(a) In general. There shall be allowed as a deduction all the ordinary "
            "and necessary expenses paid or incurred during the taxable year in "
            "carrying on any trade or business..."
        ),
        hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Subchapter B", "Section 162"],
        subsections=[
            "(a) In general",
            "(b) Charitable contributions and gifts excepted",
            "(c) Illegal bribes, kickbacks, and other payments",
            "(e) Denial of deduction for certain lobbying and political expenditures",
        ],
        effective_date=datetime(1954, 1, 1),
        source_url="https://www.law.cornell.edu/uscode/text/26/162",
        metadata={
            "version": "2024-01",
            "last_amended": "1986-10-22",
        },
    )


@pytest.fixture
def sample_tax_section_hierarchy():
    """
    Fixture providing a parent-child TaxSection hierarchy.
    """
    chapter_id = uuid4()
    chapter = TaxSection(
        id=chapter_id,
        section_number="Chapter 1",
        title="Normal Taxes and Surtaxes",
        content="This chapter contains provisions for normal taxes...",
        hierarchy=["Title 26", "Subtitle A", "Chapter 1"],
        section_type=SectionType.CHAPTER,
    )

    section = TaxSection(
        parent_id=chapter_id,
        section_number="26 U.S.C. § 162",
        title="Trade or business expenses",
        content="Full content...",
        hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Section 162"],
        section_type=SectionType.SECTION,
    )

    return chapter, section


@pytest.fixture
def sample_section_types():
    """
    Fixture providing examples of all SectionType enum values.
    """
    section_types_data = [
        (SectionType.TITLE, "Title 26", ["Title 26"]),
        (SectionType.SUBTITLE, "Subtitle A", ["Title 26", "Subtitle A"]),
        (SectionType.CHAPTER, "Chapter 1", ["Title 26", "Subtitle A", "Chapter 1"]),
        (
            SectionType.SUBCHAPTER,
            "Subchapter B",
            ["Title 26", "Subtitle A", "Chapter 1", "Subchapter B"],
        ),
        (SectionType.PART, "Part VI", ["Title 26", "Subtitle A", "Chapter 1", "Part VI"]),
        (
            SectionType.SECTION,
            "Section 162",
            ["Title 26", "Subtitle A", "Chapter 1", "Section 162"],
        ),
        (
            SectionType.SUBSECTION,
            "Subsection (a)",
            ["Title 26", "Subtitle A", "Chapter 1", "Section 162", "(a)"],
        ),
        (
            SectionType.PARAGRAPH,
            "Paragraph (1)",
            ["Title 26", "Subtitle A", "Chapter 1", "Section 162", "(a)", "(1)"],
        ),
        (
            SectionType.SUBPARAGRAPH,
            "Subparagraph (A)",
            ["Title 26", "Subtitle A", "Chapter 1", "Section 162", "(a)", "(1)", "(A)"],
        ),
    ]

    sections = []
    for section_type, number, hierarchy in section_types_data:
        section = TaxSection(
            section_number=number,
            title=f"Test {section_type.value}",
            content=f"Content for {section_type.value}",
            hierarchy=hierarchy,
            section_type=section_type,
        )
        sections.append(section)

    return sections