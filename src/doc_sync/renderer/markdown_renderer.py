"""Markdown rendering and custom-block merge (Phase 4 — T-017–T-020)."""

from __future__ import annotations

from pathlib import Path

from doc_sync.config.schema import DocSyncConfig
from doc_sync.models.documents import RepositoryIndex


class AnchorGenerator:
    """Generates GitHub-compatible heading anchor slugs (Phase 4 — T-017)."""

    def slug(self, qualified_name: str) -> str:
        raise NotImplementedError("AnchorGenerator.slug is implemented in Phase 4 (T-017)")


class TocBuilder:
    """Builds nested table-of-contents Markdown (Phase 4 — T-018)."""

    def build(self, index: RepositoryIndex, config: DocSyncConfig) -> str:
        raise NotImplementedError("TocBuilder.build is implemented in Phase 4 (T-018)")


class MarkdownRenderer:
    """Renders RepositoryIndex to Markdown file contents (Phase 4 — T-019)."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def render(self, index: RepositoryIndex) -> dict[Path, str]:
        raise NotImplementedError("MarkdownRenderer.render is implemented in Phase 4 (T-019)")


class CustomBlockMerger:
    """Merges slot-based custom Markdown blocks (Phase 4 — T-020)."""

    def merge(self, existing: str | None, generated: str) -> str:
        raise NotImplementedError("CustomBlockMerger.merge is implemented in Phase 4 (T-020)")
