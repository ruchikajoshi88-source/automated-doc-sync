"""AST metadata extractors (Phase 3 — T-012–T-016)."""

from __future__ import annotations

import ast
from pathlib import Path

from doc_sync.config.schema import DocSyncConfig
from doc_sync.models.documents import ModuleDocument, ParseIssue


def extract_module(
    tree: ast.Module,
    path: Path,
    config: DocSyncConfig,
) -> tuple[ModuleDocument, tuple[ParseIssue, ...]]:
    """Compose module, symbol, and route extractors into a ModuleDocument."""
    raise NotImplementedError("extract_module is implemented in Phase 3 (T-016)")
