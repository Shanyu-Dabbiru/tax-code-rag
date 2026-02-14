#!/usr/bin/env python3
"""Create a 10-file HTML test subset for smoke testing."""

from __future__ import annotations

import random
import shutil
import sys
from pathlib import Path

SOURCE_DIR = Path("data/USCODE-2023-title26/raw/html")
TARGET_DIR = Path("data/test_samples")
TOTAL_FILES = 10
FIRST_FILES = 5


def _collect_html_files(source_dir: Path) -> list[Path]:
	return sorted(
		[
			path
			for path in source_dir.rglob("*")
			if path.is_file() and path.suffix.lower() in (".htm", ".html")
		]
	)


def create_test_subset() -> None:
	if not SOURCE_DIR.exists():
		print(f"Source directory not found: {SOURCE_DIR}", file=sys.stderr)
		sys.exit(1)

	html_files = _collect_html_files(SOURCE_DIR)
	if len(html_files) < TOTAL_FILES:
		print(
			f"Not enough HTML files: found {len(html_files)}, need {TOTAL_FILES}",
			file=sys.stderr,
		)
		sys.exit(1)

	first_batch = html_files[:FIRST_FILES]
	remaining = html_files[FIRST_FILES:]
	random_batch = random.sample(remaining, TOTAL_FILES - FIRST_FILES)
	selected = first_batch + random_batch

	TARGET_DIR.mkdir(parents=True, exist_ok=True)

	for path in selected:
		destination = TARGET_DIR / path.name
		shutil.copy2(path, destination)

	print(f"Copied {len(selected)}/{TOTAL_FILES} files to {TARGET_DIR}")


if __name__ == "__main__":
	create_test_subset()
