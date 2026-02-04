"""
Tax data models and schemas for the RAG pipeline.

This module defines Pydantic models that structure tax code data
for consistent validation, serialization, and retrieval.
"""

from src.models.tax_data import TaxSection

__all__ = ["TaxSection"]
