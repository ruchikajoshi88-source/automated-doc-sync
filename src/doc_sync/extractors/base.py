"""Shared route-extractor helpers."""

from __future__ import annotations

from doc_sync.models.documents import ParseIssue


class RouteExtractorBase:
    """Collects per-extract warnings for FastAPI and Flask route extractors."""

    def __init__(self) -> None:
        self._warnings: list[ParseIssue] = []

    def warnings(self) -> tuple[ParseIssue, ...]:
        """Return warnings collected during the last extract call."""
        return tuple(self._warnings)

    def _reset_warnings(self) -> None:
        self._warnings.clear()

    def _warn(self, issue: ParseIssue) -> None:
        self._warnings.append(issue)
