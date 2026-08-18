"""AST parsing with encoding and size guards (Phase 3 — T-011)."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

from doc_sync.config.schema import DocSyncConfig
from doc_sync.models.documents import ParseIssue


@dataclass(frozen=True)
class ParseResult:
    """Outcome of parsing a single Python source file."""

    path: Path
    tree: ast.Module | None = None
    issue: ParseIssue | None = None

    @property
    def success(self) -> bool:
        return self.tree is not None and self.issue is None


class AstParser:
    """Parses Python source files using the standard library ast module."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def parse_file(self, path: Path) -> ParseResult:
        """Read and parse a Python file; never execute module code."""
        raise NotImplementedError("AstParser.parse_file is implemented in Phase 3 (T-011)")
