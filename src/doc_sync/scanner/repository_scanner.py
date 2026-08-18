"""Repository file discovery (Phase 2 — T-010)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from doc_sync.config.schema import DocSyncConfig


class RepositoryScanner:
    """Discovers Python source files matching include/exclude pathspec rules."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def discover_python_files(self) -> Iterator[Path]:
        """Yield absolute paths to `.py` files under repo_root."""
        raise NotImplementedError(
            "RepositoryScanner.discover_python_files is implemented in Phase 2 (T-010)"
        )
