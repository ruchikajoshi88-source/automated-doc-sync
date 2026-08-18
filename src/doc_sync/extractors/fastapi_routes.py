"""FastAPI route decorator extraction (Phase 3 — T-014)."""

from __future__ import annotations

import ast

from doc_sync.models.documents import ParseIssue, RouteDocument


class FastAPIRouteExtractor:
    """Detects @app.* and @router.* route decorators."""

    HTTP_METHODS = frozenset(
        {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
    )

    def extract(self, tree: ast.Module) -> tuple[RouteDocument, ...]:
        """Return FastAPI route metadata from literal decorator paths."""
        raise NotImplementedError(
            "FastAPIRouteExtractor.extract is implemented in Phase 3 (T-014)"
        )

    def warnings(self) -> tuple[ParseIssue, ...]:
        """Warnings collected during the last extract call."""
        return ()
