"""Extension-point protocols for extractors and renderers.

MVP implementations are duck-typed; these Protocols document the contracts so
later phases (and post-MVP plugins) can satisfy them without changing callers.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Protocol, runtime_checkable

from doc_sync.config.schema import DocSyncConfig
from doc_sync.models.documents import (
    ModuleDocument,
    ParseIssue,
    RepositoryIndex,
    RouteDocument,
    SymbolDocument,
)


@runtime_checkable
class RouteExtractor(Protocol):
    """Extract HTTP route metadata from a parsed AST module."""

    def extract(self, tree: ast.Module) -> tuple[RouteDocument, ...]:
        """Return route documents discovered in ``tree``."""
        ...

    def warnings(self) -> tuple[ParseIssue, ...]:
        """Return warnings collected during the last ``extract`` call."""
        ...


@runtime_checkable
class OutputRenderer(Protocol):
    """Render a repository index to output-path → content mappings."""

    def render(self, index: RepositoryIndex) -> dict[Path, str]:
        """Return deterministic file contents keyed by destination path."""
        ...


@runtime_checkable
class ModuleExtractorProtocol(Protocol):
    """Extract module path and module-level docstring from an AST."""

    def extract(
        self,
        tree: ast.Module,
        path: Path,
        repo_root: Path,
    ) -> tuple[str, str | None]:
        """Return ``(qualified_module_path, docstring)``."""
        ...


@runtime_checkable
class SymbolExtractorProtocol(Protocol):
    """Extract classes, functions, and methods from an AST module."""

    def extract(self, tree: ast.Module, module_path: str) -> tuple[SymbolDocument, ...]:
        """Return documented (or placeholder) symbols for ``module_path``."""
        ...


class ModuleExtractFn(Protocol):
    """Callable orchestrator that composes extractors into a ModuleDocument."""

    def __call__(
        self,
        tree: ast.Module,
        path: Path,
        config: DocSyncConfig,
    ) -> tuple[ModuleDocument, tuple[ParseIssue, ...]]:
        ...
