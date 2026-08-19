"""Orphan documentation pruning via per-run manifest."""

from __future__ import annotations

from pathlib import Path

from doc_sync.config.schema import DocSyncConfig


class StaleDocManager:
    """Orphan documentation pruning via run manifest (Phase 5 — T-022)."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def record_generated(self, path: Path) -> None:
        """Record a generated documentation path in the current-run manifest."""
        raise NotImplementedError(
            "StaleDocManager.record_generated is implemented in Phase 5 (T-022)"
        )

    def prune_orphans(self, *, force: bool = False) -> tuple[Path, ...]:
        """Remove orphan files under docs/modules/; skip custom-block files unless force."""
        raise NotImplementedError(
            "StaleDocManager.prune_orphans is implemented in Phase 5 (T-022)"
        )
