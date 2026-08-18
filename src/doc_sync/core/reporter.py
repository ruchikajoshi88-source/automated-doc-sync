"""Sync run reporting and summary output (Phase 5 — T-021)."""

from __future__ import annotations

from pathlib import Path

from doc_sync.core.sync_engine import SyncResult
from doc_sync.exceptions import EXIT_PARTIAL, EXIT_SUCCESS
from doc_sync.models.documents import ParseIssue


class SyncReporter:
    """Collects warnings and emits a run summary."""

    def __init__(self) -> None:
        self.issues: list[ParseIssue] = []
        self.processed_files = 0
        self.skipped_files = 0
        self.generated_paths: list[Path] = []
        self.updated_paths: list[Path] = []

    def record_warning(self, issue: ParseIssue) -> None:
        self.issues.append(issue)

    def build_summary(self) -> SyncResult:
        exit_code = EXIT_PARTIAL if self.issues else EXIT_SUCCESS
        return SyncResult(
            exit_code=exit_code,
            processed_files=self.processed_files,
            skipped_files=self.skipped_files,
            warnings=tuple(self.issues),
            generated_paths=tuple(self.generated_paths),
            updated_paths=tuple(self.updated_paths),
        )

    def emit_summary(self, result: SyncResult) -> None:
        import sys

        print(
            f"doc-sync: processed={result.processed_files} "
            f"skipped={result.skipped_files} warnings={result.warning_count} "
            f"generated={result.generated_count} updated={result.updated_count}",
            file=sys.stderr,
        )
