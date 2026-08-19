"""Slot-based custom Markdown block preservation."""

from __future__ import annotations


class CustomBlockMerger:
    """Merges slot-based custom Markdown blocks (Phase 4 — T-020)."""

    def merge(self, existing: str | None, generated: str) -> str:
        """Splice preserved custom slots into generated Markdown; raise DocMergeError on invalid markers."""
        raise NotImplementedError("CustomBlockMerger.merge is implemented in Phase 4 (T-020)")
