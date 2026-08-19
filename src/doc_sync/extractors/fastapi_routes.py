"""FastAPI route decorator extraction (Phase 3 — T-014)."""

from __future__ import annotations

import ast

from doc_sync.extractors.base import RouteExtractorBase
from doc_sync.models.documents import RouteDocument


class FastAPIRouteExtractor(RouteExtractorBase):
    """Detects @app.* and @router.* route decorators."""

    HTTP_METHODS = frozenset(
        {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
    )

    def extract(self, tree: ast.Module) -> tuple[RouteDocument, ...]:
        """Return FastAPI route metadata from literal decorator paths."""
        self._reset_warnings()
        raise NotImplementedError(
            "FastAPI route extraction is not yet implemented."
        )
