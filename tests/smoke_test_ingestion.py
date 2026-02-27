#!/usr/bin/env python3
"""Smoke test for ingestion pipeline with OpenTelemetry tracing."""

from __future__ import annotations

import sys
from pathlib import Path

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.parser import TaxParser

TEST_DIR = Path("data/test_samples")
TOTAL_FILES = 10


def _install_inmemory_exporter() -> InMemorySpanExporter:
	exporter = InMemorySpanExporter()
	provider = trace.get_tracer_provider()
	if isinstance(provider, TracerProvider):
		provider.add_span_processor(SimpleSpanProcessor(exporter))
	return exporter





def run_smoke_test() -> None:
	if not TEST_DIR.exists():
		print("Test samples not found. Run scripts/create_test_subset.py first.")
		sys.exit(1)

	# Setup an in-memory tracer provider instead of OTLP exporter to avoid hanging
	provider = TracerProvider()
	trace.set_tracer_provider(provider)
	exporter = _install_inmemory_exporter()

	parser = TaxParser(root_dir=str(TEST_DIR))
	sections = parser.parse_directory()
	print(f"Successfully parsed {len(sections)}/{TOTAL_FILES} files.")

	if not sections:
		print("No sections parsed.")
		sys.exit(1)

	first = sections[0]
	preview = first.content[:100].replace("\n", " ")
	print(f"Section Number: {first.section_number}")
	print(f"Title: {first.title}")
	print(f"Content Preview: {preview}")

	output_path = TEST_DIR / "taxes.jsonl"
	if output_path.exists():
		output_path.unlink()

	parser.save_to_jsonl(sections, str(output_path))
	
	if output_path.exists() and output_path.stat().st_size > 0:
		print("Verified taxes.jsonl was successfully created.")
	else:
		print("Error: taxes.jsonl missing or empty.")
		sys.exit(1)


if __name__ == "__main__":
	run_smoke_test()
