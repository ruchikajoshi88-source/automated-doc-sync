"""Exclusive sync run lock with stale TTL."""

from __future__ import annotations

from pathlib import Path
from types import TracebackType


class RunLock:
    """Exclusive sync run lock file (Phase 2 — T-008)."""

    STALE_TTL_SECONDS = 300
    LOCK_FILENAME = ".doc-sync.lock"

    def __init__(self, lock_path: Path) -> None:
        self._lock_path = lock_path

    def __enter__(self) -> RunLock:
        raise NotImplementedError("RunLock is implemented in Phase 2 (T-008)")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError("RunLock is implemented in Phase 2 (T-008)")
