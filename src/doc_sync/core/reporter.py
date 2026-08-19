"""Sync run reporting and summary output (Phase 5 — T-021)."""

from __future__ import annotations

from pathlib import Path

from doc_sync.core.sync_engine import SyncResult
from doc_sync.exceptions import EXIT_FAILURE, EXIT_PARTIAL, EXIT_SUCCESS, DocSyncError
from doc_sync.models.documents import ParseIssue


class SyncReporter:
    """Collects warnings and blocking errors, then emits a run summary."""

    def __init__(self) -> None:
        self.issues: list[ParseIssue] = []
        self.processed_files = 0
        self.skipped_files = 0
        self.generated_paths: list[Path] = []
        self.updated_paths: list[Path] = []
        self._blocking_error: DocSyncError | None = None

    def record_warning(self, issue: ParseIssue) -> None:
        self.issues.append(issue)

    def record_blocking_error(self, error: DocSyncError) -> None:
        """Record a merge/write/lock failure that must map to exit code 1."""
        self._blocking_error = error

    @property
    def blocking_error(self) -> DocSyncError | None:
        return self._blocking_error

    def build_summary(self) -> SyncResult:
        if self._blocking_error is not None:
            exit_code = EXIT_FAILURE
        elif self.issues:
            exit_code = EXIT_PARTIAL
        else:
            exit_code = EXIT_SUCCESS
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
        if self._blocking_error is not None:
            print(f"doc-sync: error: {self._blocking_error}", file=sys.stderr)
