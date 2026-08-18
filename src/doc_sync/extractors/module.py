"""Module-level docstring and path extraction (Phase 3 — T-012)."""

from __future__ import annotations

import ast
from pathlib import Path


class ModuleExtractor:
    """Extracts module docstring and qualified module name from an AST."""

    def extract(self, tree: ast.Module, path: Path, repo_root: Path) -> tuple[str, str | None]:
        """Return (module_path, docstring)."""
        raise NotImplementedError("ModuleExtractor.extract is implemented in Phase 3 (T-012)")
