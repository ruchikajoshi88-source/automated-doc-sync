"""Stable GitHub-style heading anchor generation."""

from __future__ import annotations


class AnchorGenerator:
    """Generates GitHub-compatible heading anchor slugs (Phase 4 — T-017)."""

    def slug(self, qualified_name: str) -> str:
        """Return a lowercase, hyphenated, collision-safe heading slug."""
        raise NotImplementedError("AnchorGenerator.slug is implemented in Phase 4 (T-017)")
