"""Atomic Markdown file writes (temp file + os.replace)."""

from __future__ import annotations

from pathlib import Path

from doc_sync.io.path_validator import PathValidator


class DocumentationWriter:
    """Atomic Markdown file writer (Phase 2 — T-009)."""

    def __init__(self, validator: PathValidator) -> None:
        self._validator = validator

    def write(self, path: Path, content: str) -> None:
        """Write content atomically after validating the destination path."""
        raise NotImplementedError(
            "DocumentationWriter.write is implemented in Phase 2 (T-009)"
        )
