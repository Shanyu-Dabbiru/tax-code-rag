"""
Unit tests for TaxSection Pydantic model.

These tests aim for full coverage of model behavior, validation,
serialization, and schema generation.
"""

import json
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from src.models.tax_data import TaxSection, SectionType


class TestTaxSectionCreation:
    """Test basic TaxSection instantiation and required fields."""

    def test_create_with_minimal_required_fields(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Trade or business expenses",
            content="Full text of the section goes here.",
            hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Section 162"],
        )

        assert section.section_number == "26 U.S.C. § 162"
        assert section.title == "Trade or business expenses"
        assert section.content == "Full text of the section goes here."
        assert section.hierarchy == ["Title 26", "Subtitle A", "Chapter 1", "Section 162"]

    def test_create_with_all_fields(self):
        test_id = uuid4()
        parent_id = uuid4()
        test_date = datetime(2024, 1, 15, 10, 30, 0)
        effective_date = datetime(1954, 1, 1)

        section = TaxSection(
            id=test_id,
            parent_id=parent_id,
            section_number="26 U.S.C. § 162",
            title="Trade or business expenses",
            content="(a) In general. There shall be allowed...",
            hierarchy=["Title 26", "Subtitle A", "Chapter 1", "Section 162"],
            section_type=SectionType.SECTION,
            subsections=["(a) In general", "(b) Charitable contributions"],
            effective_date=effective_date,
            source_url="https://www.law.cornell.edu/uscode/text/26/162",
            metadata={"version": "2024-01", "last_amended": "1986-10-22"},
            created_at=test_date,
        )

        assert section.id == test_id
        assert section.parent_id == parent_id
        assert section.section_type == SectionType.SECTION
        assert section.subsections == ["(a) In general", "(b) Charitable contributions"]
        assert section.effective_date == effective_date
        assert section.source_url == "https://www.law.cornell.edu/uscode/text/26/162"
        assert section.metadata == {"version": "2024-01", "last_amended": "1986-10-22"}
        assert section.created_at == test_date

    def test_missing_required_fields_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Trade or business expenses",
            )

        errors = exc_info.value.errors()
        error_fields = {error["loc"][0] for error in errors}
        assert "content" in error_fields
        assert "hierarchy" in error_fields


class TestTaxSectionDefaultValues:
    """Test default value generation for optional fields."""

    def test_id_auto_generated_as_uuid(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Trade or business expenses",
            content="Content here",
            hierarchy=["Title 26"],
        )

        assert isinstance(section.id, UUID)
        assert section.id.version == 4

    def test_parent_id_defaults_to_none(self):
        section = TaxSection(
            section_number="26 U.S.C. § 1",
            title="Root section",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section.parent_id is None

    def test_section_type_defaults_to_section(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section.section_type == SectionType.SECTION

    def test_subsections_defaults_to_empty_list(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section.subsections == []
        assert isinstance(section.subsections, list)

    def test_metadata_defaults_to_empty_dict(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section.metadata == {}
        assert isinstance(section.metadata, dict)

    def test_created_at_auto_generated(self):
        before = datetime.now(timezone.utc)
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )
        after = datetime.now(timezone.utc)

        assert isinstance(section.created_at, datetime)
        assert section.created_at.tzinfo is not None
        assert before <= section.created_at <= after

    def test_effective_date_defaults_to_none(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section.effective_date is None

    def test_source_url_defaults_to_none(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section.source_url is None


class TestTaxSectionTypeValidation:
    """Test type validation for all fields."""

    def test_section_number_must_be_string(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number=162,
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "section_number" for error in errors)

    def test_title_must_be_string(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title=123,
                content="Content",
                hierarchy=["Title 26"],
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "title" for error in errors)

    def test_content_must_be_string(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content=["not", "a", "string"],
                hierarchy=["Title 26"],
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "content" for error in errors)

    def test_hierarchy_must_be_list(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy="Title 26",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "hierarchy" for error in errors)

    def test_hierarchy_elements_must_be_strings(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26", 1, "Chapter 1"],
            )

        errors = exc_info.value.errors()
        assert any("hierarchy" in str(error["loc"]) for error in errors)

    def test_subsections_must_be_list(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
                subsections="(a) In general",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "subsections" for error in errors)

    def test_metadata_must_be_dict(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
                metadata=["not", "a", "dict"],
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "metadata" for error in errors)

    def test_id_must_be_uuid(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                id="not-a-uuid",
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "id" for error in errors)

    def test_parent_id_must_be_uuid_or_none(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                parent_id="not-a-uuid",
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "parent_id" for error in errors)

    def test_section_type_must_be_valid_enum(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
                section_type="invalid_type",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "section_type" for error in errors)

    def test_effective_date_must_be_datetime_or_none(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
            effective_date="2024-01-01",
        )

        assert isinstance(section.effective_date, datetime)

    def test_source_url_must_be_string_or_none(self):
        with pytest.raises(ValidationError) as exc_info:
            TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
                source_url=12345,
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "source_url" for error in errors)


class TestSectionTypeEnum:
    """Test SectionType enum behavior."""

    def test_all_section_types_are_valid(self):
        valid_types = [
            SectionType.TITLE,
            SectionType.SUBTITLE,
            SectionType.CHAPTER,
            SectionType.SUBCHAPTER,
            SectionType.PART,
            SectionType.SECTION,
            SectionType.SUBSECTION,
            SectionType.PARAGRAPH,
            SectionType.SUBPARAGRAPH,
        ]

        for section_type in valid_types:
            section = TaxSection(
                section_number="26 U.S.C. § 162",
                title="Test",
                content="Content",
                hierarchy=["Title 26"],
                section_type=section_type,
            )
            assert section.section_type == section_type

    def test_section_type_string_values(self):
        assert SectionType.TITLE.value == "title"
        assert SectionType.SUBTITLE.value == "subtitle"
        assert SectionType.CHAPTER.value == "chapter"
        assert SectionType.SUBCHAPTER.value == "subchapter"
        assert SectionType.PART.value == "part"
        assert SectionType.SECTION.value == "section"
        assert SectionType.SUBSECTION.value == "subsection"
        assert SectionType.PARAGRAPH.value == "paragraph"
        assert SectionType.SUBPARAGRAPH.value == "subparagraph"

    def test_section_type_can_be_created_from_string(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
            section_type="chapter",
        )
        assert section.section_type == SectionType.CHAPTER


class TestTaxSectionSerialization:
    """Test JSON serialization and deserialization."""

    def test_serialize_to_dict(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Trade or business expenses",
            content="Full text here",
            hierarchy=["Title 26", "Subtitle A", "Chapter 1"],
        )

        section_dict = section.model_dump()

        assert isinstance(section_dict, dict)
        assert section_dict["section_number"] == "26 U.S.C. § 162"
        assert section_dict["title"] == "Trade or business expenses"
        assert section_dict["content"] == "Full text here"
        assert section_dict["hierarchy"] == ["Title 26", "Subtitle A", "Chapter 1"]
        assert isinstance(section_dict["id"], UUID)

    def test_serialize_to_json(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Trade or business expenses",
            content="Full text here",
            hierarchy=["Title 26", "Subtitle A"],
        )

        json_str = section.model_dump_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["section_number"] == "26 U.S.C. § 162"
        assert parsed["title"] == "Trade or business expenses"

    def test_deserialize_from_dict(self):
        test_id = str(uuid4())
        data = {
            "id": test_id,
            "section_number": "26 U.S.C. § 162",
            "title": "Trade or business expenses",
            "content": "Full text here",
            "hierarchy": ["Title 26", "Subtitle A", "Chapter 1"],
            "section_type": "section",
            "subsections": ["(a) In general"],
            "metadata": {"version": "2024-01"},
        }

        section = TaxSection(**data)

        assert str(section.id) == test_id
        assert section.section_number == "26 U.S.C. § 162"
        assert section.title == "Trade or business expenses"
        assert section.subsections == ["(a) In general"]
        assert section.metadata == {"version": "2024-01"}

    def test_deserialize_from_json(self):
        json_data = """
        {
            "section_number": "26 U.S.C. § 162",
            "title": "Trade or business expenses",
            "content": "Full text here",
            "hierarchy": ["Title 26", "Subtitle A", "Chapter 1"]
        }
        """

        section = TaxSection.model_validate_json(json_data)

        assert section.section_number == "26 U.S.C. § 162"
        assert section.title == "Trade or business expenses"
        assert section.content == "Full text here"
        assert section.hierarchy == ["Title 26", "Subtitle A", "Chapter 1"]

    def test_round_trip_serialization(self):
        original = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Trade or business expenses",
            content="Full text here",
            hierarchy=["Title 26", "Subtitle A", "Chapter 1"],
            subsections=["(a) In general", "(b) Charitable contributions"],
            metadata={"version": "2024-01"},
        )

        json_str = original.model_dump_json()
        restored = TaxSection.model_validate_json(json_str)

        assert restored.id == original.id
        assert restored.section_number == original.section_number
        assert restored.title == original.title
        assert restored.content == original.content
        assert restored.hierarchy == original.hierarchy
        assert restored.subsections == original.subsections
        assert restored.metadata == original.metadata


class TestTaxSectionEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_hierarchy_list(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=[],
        )

        assert section.hierarchy == []

    def test_single_element_hierarchy(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section.hierarchy == ["Title 26"]
        assert len(section.hierarchy) == 1

    def test_deep_hierarchy(self):
        deep_hierarchy = [
            "Title 26",
            "Subtitle A",
            "Chapter 1",
            "Subchapter B",
            "Part VI",
            "Section 162",
            "Subsection (a)",
            "Paragraph (1)",
            "Subparagraph (A)",
        ]

        section = TaxSection(
            section_number="26 U.S.C. § 162(a)(1)(A)",
            title="Test",
            content="Content",
            hierarchy=deep_hierarchy,
        )

        assert section.hierarchy == deep_hierarchy
        assert len(section.hierarchy) == 9

    def test_empty_content_string(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="",
            hierarchy=["Title 26"],
        )

        assert section.content == ""

    def test_long_content_string(self):
        long_content = "A" * 100000

        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content=long_content,
            hierarchy=["Title 26"],
        )

        assert len(section.content) == 100000

    def test_many_subsections(self):
        many_subsections = [f"({chr(97 + i)}) Subsection {i}" for i in range(26)]

        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
            subsections=many_subsections,
        )

        assert len(section.subsections) == 26

    def test_special_characters_in_strings(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162(a)(1)(A)",
            title="Trade & Business—Expenses (Special: €$¥£)",
            content="Content with special chars: <>&\"'\n\t",
            hierarchy=["Title 26", "Subtitle A—Income Taxes"],
        )

        assert "§" in section.section_number
        assert "€$¥£" in section.title
        assert "<>&\"'" in section.content

    def test_unicode_content(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test Unicode: 中文 日本語 한국어",
            content="Content with emoji: 🏛️ 📚 💼",
            hierarchy=["Title 26"],
        )

        assert "中文" in section.title
        assert "🏛️" in section.content

    def test_metadata_with_various_value_types(self):
        section = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
            metadata={
                "version": "2024-01",
                "status": "active",
                "notes": "Sample notes",
            },
        )

        assert section.metadata["version"] == "2024-01"
        assert section.metadata["status"] == "active"


class TestTaxSectionEquality:
    """Test equality and comparison operations."""

    def test_sections_with_same_id_are_equal(self):
        test_id = uuid4()

        section1 = TaxSection(
            id=test_id,
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        section2 = TaxSection(
            id=test_id,
            section_number="Different number",
            title="Different title",
            content="Different content",
            hierarchy=["Different hierarchy"],
        )

        assert section1.id == section2.id

    def test_sections_with_different_ids_are_not_equal(self):
        section1 = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        section2 = TaxSection(
            section_number="26 U.S.C. § 162",
            title="Test",
            content="Content",
            hierarchy=["Title 26"],
        )

        assert section1.id != section2.id
        assert section1 != section2


class TestTaxSectionSchema:
    """Test JSON schema generation."""

    def test_json_schema_generation(self):
        schema = TaxSection.model_json_schema()

        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "required" in schema

        required_fields = schema["required"]
        assert "section_number" in required_fields
        assert "title" in required_fields
        assert "content" in required_fields
        assert "hierarchy" in required_fields

    def test_schema_includes_all_fields(self):
        schema = TaxSection.model_json_schema()
        properties = schema["properties"]

        expected_fields = [
            "id",
            "parent_id",
            "section_number",
            "title",
            "content",
            "hierarchy",
            "section_type",
            "subsections",
            "effective_date",
            "source_url",
            "metadata",
            "created_at",
        ]

        for field in expected_fields:
            assert field in properties, f"Field '{field}' missing from schema"

    def test_schema_has_definitions(self):
        schema = TaxSection.model_json_schema()
        assert "$defs" in schema