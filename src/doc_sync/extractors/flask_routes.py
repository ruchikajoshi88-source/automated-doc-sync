"""Flask route decorator extraction (Phase 3 — T-015)."""

from __future__ import annotations

import ast

from doc_sync.models.documents import ParseIssue, RouteDocument


class FlaskRouteExtractor:
    """Detects @app.route and @blueprint.route decorators."""

    def extract(self, tree: ast.Module) -> tuple[RouteDocument, ...]:
        """Return Flask route metadata from literal decorator rules."""
        raise NotImplementedError(
            "FlaskRouteExtractor.extract is implemented in Phase 3 (T-015)"
        )

    def warnings(self) -> tuple[ParseIssue, ...]:
        """Warnings collected during the last extract call."""
        return ()
