"""Nested table-of-contents generation from a repository index."""

from __future__ import annotations

from doc_sync.config.schema import DocSyncConfig
from doc_sync.models.documents import RepositoryIndex


class TocBuilder:
    """Builds nested table-of-contents Markdown (Phase 4 — T-018)."""

    def build(self, index: RepositoryIndex, config: DocSyncConfig) -> str:
        """Return nested TOC Markdown linking to module pages and in-page anchors."""
        raise NotImplementedError("TocBuilder.build is implemented in Phase 4 (T-018)")
