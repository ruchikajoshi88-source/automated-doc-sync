"""Filesystem I/O, path sandbox, and run locking (Phase 2 — T-007–T-009, T-022)."""

from __future__ import annotations

from pathlib import Path

from doc_sync.config.schema import DocSyncConfig


class PathValidator:
    """Validates paths against the output sandbox (Phase 2 — T-007)."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def resolve_output_path(self, module_path: str) -> Path:
        raise NotImplementedError(
            "PathValidator.resolve_output_path is implemented in Phase 2 (T-007)"
        )

    def validate_write_path(self, path: Path) -> Path:
        raise NotImplementedError(
            "PathValidator.validate_write_path is implemented in Phase 2 (T-007)"
        )


class DocumentationWriter:
    """Atomic Markdown file writer (Phase 2 — T-009)."""

    def __init__(self, validator: PathValidator) -> None:
        self._validator = validator

    def write(self, path: Path, content: str) -> None:
        raise NotImplementedError(
            "DocumentationWriter.write is implemented in Phase 2 (T-009)"
        )


class StaleDocManager:
    """Orphan documentation pruning via run manifest (Phase 5 — T-022)."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def record_generated(self, path: Path) -> None:
        raise NotImplementedError(
            "StaleDocManager.record_generated is implemented in Phase 5 (T-022)"
        )

    def prune_orphans(self, *, force: bool = False) -> tuple[Path, ...]:
        raise NotImplementedError(
            "StaleDocManager.prune_orphans is implemented in Phase 5 (T-022)"
        )


class RunLock:
    """Exclusive sync run lock file (Phase 2 — T-008)."""

    STALE_TTL_SECONDS = 300

    def __init__(self, lock_path: Path) -> None:
        self._lock_path = lock_path

    def __enter__(self) -> RunLock:
        raise NotImplementedError("RunLock is implemented in Phase 2 (T-008)")

    def __exit__(self, *args: object) -> None:
        raise NotImplementedError("RunLock is implemented in Phase 2 (T-008)")
