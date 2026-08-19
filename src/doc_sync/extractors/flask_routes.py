"""Flask route decorator extraction (Phase 3 — T-015)."""

from __future__ import annotations

import ast

from doc_sync.extractors.base import RouteExtractorBase
from doc_sync.models.documents import RouteDocument


class FlaskRouteExtractor(RouteExtractorBase):
    """Detects @app.route and @blueprint.route decorators."""

    def extract(self, tree: ast.Module) -> tuple[RouteDocument, ...]:
        """Return Flask route metadata from literal decorator rules."""
        self._reset_warnings()
        raise NotImplementedError(
            "Flask route extraction is not yet implemented."
        )
