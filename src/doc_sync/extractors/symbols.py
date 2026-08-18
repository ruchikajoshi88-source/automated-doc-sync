"""Class, function, and method extraction (Phase 3 — T-013)."""

from __future__ import annotations

import ast

from doc_sync.config.schema import DocSyncConfig
from doc_sync.models.documents import SymbolDocument


class SymbolExtractor:
    """Extracts documented symbols and type hints from an AST module."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def extract(self, tree: ast.Module, module_path: str) -> tuple[SymbolDocument, ...]:
        """Return all public symbols for the module."""
        raise NotImplementedError("SymbolExtractor.extract is implemented in Phase 3 (T-013)")
