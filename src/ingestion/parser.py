"""
HTML parser for Title 26 (Internal Revenue Code) files.

This module implements a batch TaxParser that walks the raw HTML corpus,
extracts hierarchy and content using comment regexes, and returns validated
TaxSection objects.
"""

from __future__ import annotations

import logging
import os
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Tuple

from lxml import html

from src.models.tax_data import SectionType, TaxSection


LOGGER = logging.getLogger(__name__)


DOCUMENT_ID_RE = re.compile(
	r"<!--\s*documentid:(\S+)\s+usckey:(\S+)\s+currentthrough:(\d{8})\s+"
	r"documentPDFPage:(\d+)\s*-->"
)
ITEM_PATH_RE = re.compile(r"<!--\s*itempath:([^\r\n]*?)\s*-->")
FIELD_START_RE = re.compile(r"<!--\s*field-start:([a-z0-9\-]+)\s*-->")


@dataclass(frozen=True)
class ParseResult:
	"""Internal parsing result for a single file."""

	section: Optional[TaxSection]
	skipped: bool


class TaxParser:
	"""
	Batch parser for Title 26 HTML files.

	Usage:
		parser = TaxParser(root_dir="data/USCODE-2023-title26/raw/html")
		sections = parser.parse_directory()
	"""

	def __init__(self, root_dir: str, max_workers: Optional[int] = None) -> None:
		self.root_dir = root_dir
		self.max_workers = max_workers

	def parse_directory(self) -> List[TaxSection]:
		"""Parse all HTML files in the root directory using process parallelism."""
		html_files = list(self._iter_html_files(self.root_dir))
		if not html_files:
			LOGGER.warning("No HTML files found under %s", self.root_dir)
			return []

		sections: List[TaxSection] = []
		with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
			futures = {executor.submit(self.parse_file, path): path for path in html_files}
			for future in as_completed(futures):
				result = future.result()
				if result.section is not None:
					sections.append(result.section)

		return sections

	@staticmethod
	def parse_file(file_path: str) -> ParseResult:
		"""Parse a single HTML file into a TaxSection or return skipped result."""
		with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
			raw_html = handle.read()

		metadata = TaxParser._extract_document_metadata(raw_html)
		itempath = TaxParser._extract_itempath(raw_html)
		hierarchy = TaxParser._parse_hierarchy(itempath)
		field_blocks = TaxParser._extract_field_blocks(raw_html)

		statute_html = field_blocks.get("statute")
		if not statute_html or not statute_html.strip():
			TaxParser._trace_missing_statute(file_path, metadata, itempath)
			return ParseResult(section=None, skipped=True)

		content = TaxParser._html_to_text(statute_html)
		effective_date = TaxParser._parse_effective_date(
			field_blocks.get("effectivedate-note")
		)
		section_number = TaxParser._derive_section_number(itempath, metadata)
		title = TaxParser._derive_title(field_blocks, raw_html, hierarchy)
		section_type = TaxParser._derive_section_type(hierarchy)
		subsections = TaxParser._extract_subsections(content)

		section = TaxSection(
			section_number=section_number,
			title=title,
			content=content,
			hierarchy=hierarchy,
			section_type=section_type,
			subsections=subsections,
			effective_date=effective_date,
			source_url=metadata.get("source_url"),
			metadata={k: v for k, v in metadata.items() if v is not None},
		)
		return ParseResult(section=section, skipped=False)

	@staticmethod
	def _iter_html_files(root_dir: str) -> Iterable[str]:
		for dirpath, _, filenames in os.walk(root_dir):
			for filename in filenames:
				if filename.lower().endswith((".htm", ".html")):
					yield os.path.join(dirpath, filename)

	@staticmethod
	def _extract_document_metadata(raw_html: str) -> Dict[str, Optional[str]]:
		match = DOCUMENT_ID_RE.search(raw_html)
		if not match:
			return {
				"documentid": None,
				"usckey": None,
				"currentthrough": None,
				"documentPDFPage": None,
				"source_url": None,
			}

		documentid, usckey, currentthrough, pdf_page = match.groups()
		return {
			"documentid": documentid,
			"usckey": usckey,
			"currentthrough": currentthrough,
			"documentPDFPage": pdf_page,
			"source_url": None,
		}

	@staticmethod
	def _extract_itempath(raw_html: str) -> str:
		match = ITEM_PATH_RE.search(raw_html)
		return match.group(1).strip() if match else ""

	@staticmethod
	def _extract_field_blocks(raw_html: str) -> Dict[str, str]:
		blocks: Dict[str, str] = {}
		matches = list(FIELD_START_RE.finditer(raw_html))
		for idx, match in enumerate(matches):
			field_name = match.group(1)
			start = match.end()
			end = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw_html)
			blocks[field_name] = raw_html[start:end]
		return blocks

	@staticmethod
	def _html_to_text(fragment: str) -> str:
		try:
			doc = html.fromstring(fragment)
			return " ".join(doc.text_content().split())
		except (ValueError, TypeError):
			return " ".join(fragment.split())

	@staticmethod
	def _parse_hierarchy(itempath: str) -> List[str]:
		if not itempath:
			return []
		parts = [p for p in itempath.strip("/").split("/") if p]
		normalized: List[str] = []
		for part in parts:
			if part.isdigit():
				normalized.append(f"Title {int(part)}")
				continue
			cleaned = part.strip()
			cleaned = cleaned.replace("CHAPTER", "Chapter")
			cleaned = cleaned.replace("PART", "Part")
			cleaned = cleaned.replace("SUBTITLE", "Subtitle")
			cleaned = cleaned.replace("SUBCHAPTER", "Subchapter")
			cleaned = cleaned.replace("Sec.", "Section")
			normalized.append(cleaned)
		return normalized

	@staticmethod
	def _derive_section_number(itempath: str, metadata: Dict[str, Optional[str]]) -> str:
		section_match = re.search(r"Sec\.\s*(\d+[A-Za-z0-9\-]*)", itempath)
		if section_match:
			section_id = section_match.group(1)
			return f"26 U.S.C. § {section_id}"

		documentid = metadata.get("documentid")
		if documentid and "_" in documentid:
			_, section_id = documentid.split("_", 1)
			return f"26 U.S.C. § {section_id}"

		return "26 U.S.C. § Unknown"

	@staticmethod
	def _derive_title(
		field_blocks: Dict[str, str], raw_html: str, hierarchy: List[str]
	) -> str:
		if "head" in field_blocks:
			head_text = TaxParser._html_to_text(field_blocks["head"])
			if head_text:
				return head_text

		try:
			doc = html.fromstring(raw_html)
			title_nodes = doc.xpath("//title")
			if title_nodes:
				return " ".join(title_nodes[0].text_content().split())
		except (ValueError, TypeError):
			pass

		return hierarchy[-1] if hierarchy else "Untitled"

	@staticmethod
	def _derive_section_type(hierarchy: List[str]) -> SectionType:
		if not hierarchy:
			return SectionType.SECTION
		last = hierarchy[-1].lower()
		if last.startswith("title"):
			return SectionType.TITLE
		if last.startswith("subtitle"):
			return SectionType.SUBTITLE
		if last.startswith("chapter"):
			return SectionType.CHAPTER
		if last.startswith("subchapter"):
			return SectionType.SUBCHAPTER
		if last.startswith("part"):
			return SectionType.PART
		if last.startswith("section"):
			return SectionType.SECTION
		if last.startswith("subsection"):
			return SectionType.SUBSECTION
		if last.startswith("paragraph"):
			return SectionType.PARAGRAPH
		if last.startswith("subparagraph"):
			return SectionType.SUBPARAGRAPH
		return SectionType.SECTION

	@staticmethod
	def _extract_subsections(content: str) -> List[str]:
		if not content:
			return []
		pattern = re.compile(r"\((\w+)\)\s+[^\n]+")
		results = []
		for match in pattern.finditer(content):
			results.append(match.group(0).strip())
		return results

	@staticmethod
	def _parse_effective_date(effectivedate_html: Optional[str]) -> Optional[datetime]:
		if not effectivedate_html:
			return None
		text = TaxParser._html_to_text(effectivedate_html)
		date_match = re.search(r"(\d{4})[-/](\d{2})[-/](\d{2})", text)
		if date_match:
			return datetime(
				int(date_match.group(1)),
				int(date_match.group(2)),
				int(date_match.group(3)),
				tzinfo=timezone.utc,
			)
		date_match = re.search(r"(\d{8})", text)
		if date_match:
			value = date_match.group(1)
			return datetime.strptime(value, "%Y%m%d").replace(tzinfo=timezone.utc)
		return None

	@staticmethod
	def _trace_missing_statute(
		file_path: str, metadata: Dict[str, Optional[str]], itempath: str
	) -> None:
		try:
			from opentelemetry import trace

			tracer = trace.get_tracer(__name__)
			with tracer.start_as_current_span("missing_statute") as span:
				span.set_attribute("file_path", file_path)
				span.set_attribute("itempath", itempath)
				for key, value in metadata.items():
					if value is not None:
						span.set_attribute(key, value)
		except Exception:
			LOGGER.warning(
				"Missing statute field in %s (itempath=%s, metadata=%s)",
				file_path,
				itempath,
				metadata,
			)
