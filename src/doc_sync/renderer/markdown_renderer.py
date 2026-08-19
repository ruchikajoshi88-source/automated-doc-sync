"""Markdown rendering of repository indexes into module pages and API.md."""

from __future__ import annotations

from pathlib import Path

from doc_sync.config.schema import DocSyncConfig
from doc_sync.models.documents import RepositoryIndex


class MarkdownRenderer:
    """Renders RepositoryIndex to Markdown file contents (Phase 4 — T-019)."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def render(self, index: RepositoryIndex) -> dict[Path, str]:
        """Return a mapping of output paths to deterministic Markdown content."""
        raise NotImplementedError("MarkdownRenderer.render is implemented in Phase 4 (T-019)")
