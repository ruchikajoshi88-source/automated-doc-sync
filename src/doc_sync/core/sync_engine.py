"""Sync pipeline result and orchestration types."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from doc_sync.config.schema import DocSyncConfig
from doc_sync.exceptions import EXIT_SUCCESS
from doc_sync.models.documents import ParseIssue


@dataclass(frozen=True)
class SyncResult:
    """Outcome of a documentation sync run."""

    exit_code: int = EXIT_SUCCESS
    processed_files: int = 0
    skipped_files: int = 0
    warnings: tuple[ParseIssue, ...] = ()
    generated_paths: tuple[Path, ...] = ()
    updated_paths: tuple[Path, ...] = ()

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def generated_count(self) -> int:
        return len(self.generated_paths)

    @property
    def updated_count(self) -> int:
        return len(self.updated_paths)


class SyncEngine:
    """End-to-end documentation sync orchestrator (Phase 5 — T-023)."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def run(self, *, stage: bool = False, force_prune: bool = False, full: bool = True) -> SyncResult:
        """Execute the full sync pipeline."""
        raise NotImplementedError("SyncEngine.run is implemented in Phase 5 (T-023)")
