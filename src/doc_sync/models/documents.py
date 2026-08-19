"""Immutable domain models for extracted documentation metadata."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Sequence

from doc_sync.exceptions import Severity


class SymbolKind(str, Enum):
    """Kind of documented Python symbol."""

    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    PROPERTY = "property"


class RouteFramework(str, Enum):
    """Web framework identifier for route metadata."""

    FASTAPI = "fastapi"
    FLASK = "flask"


class ParameterKind(str, Enum):
    """Function parameter kind for signature rendering."""

    POSITIONAL_ONLY = "positional_only"
    POSITIONAL_OR_KEYWORD = "positional_or_keyword"
    VAR_POSITIONAL = "var_positional"
    KEYWORD_ONLY = "keyword_only"
    VAR_KEYWORD = "var_keyword"


@dataclass(frozen=True)
class ParameterDoc:
    """Documented function or method parameter."""

    name: str
    annotation: str | None = None
    default_repr: str | None = None
    kind: ParameterKind = ParameterKind.POSITIONAL_OR_KEYWORD

    def sort_key(self) -> tuple[str, str]:
        return (self.kind.value, self.name)


@dataclass(frozen=True)
class SymbolDocument:
    """Documented class, function, method, or property."""

    kind: SymbolKind
    name: str
    qualified_name: str
    docstring: str | None = None
    parameters: tuple[ParameterDoc, ...] = ()
    return_annotation: str | None = None
    is_async: bool = False
    decorators: tuple[str, ...] = ()

    @property
    def is_placeholder(self) -> bool:
        """True when docstring was absent and a stub entry was generated."""
        return self.docstring is None

    def sort_key(self) -> tuple[object, ...]:
        return (
            self.kind.value,
            self.qualified_name,
            tuple(p.sort_key() for p in self.parameters),
            self.return_annotation or "",
        )


@dataclass(frozen=True)
class RouteDocument:
    """Documented FastAPI or Flask route."""

    framework: RouteFramework
    methods: tuple[str, ...]
    path: str
    handler_name: str
    summary: str | None = None

    def sort_key(self) -> tuple[str, ...]:
        primary_method = self.methods[0] if self.methods else ""
        return (self.path, primary_method, self.handler_name, self.framework.value)


@dataclass(frozen=True)
class ModuleDocument:
    """Documentation extracted from a single Python module."""

    module_path: str
    source_relpath: str
    docstring: str | None = None
    symbols: tuple[SymbolDocument, ...] = ()
    routes: tuple[RouteDocument, ...] = ()

    def sort_key(self) -> tuple[object, ...]:
        return (
            self.module_path,
            tuple(s.sort_key() for s in self.sorted_symbols),
            tuple(r.sort_key() for r in self.sorted_routes),
        )

    @property
    def sorted_symbols(self) -> tuple[SymbolDocument, ...]:
        return tuple(sorted(self.symbols, key=lambda s: s.sort_key()))

    @property
    def sorted_routes(self) -> tuple[RouteDocument, ...]:
        return tuple(sorted(self.routes, key=lambda r: r.sort_key()))

    def with_sorted_collections(self) -> ModuleDocument:
        """Return a copy with symbols and routes in deterministic order."""
        return replace(self, symbols=self.sorted_symbols, routes=self.sorted_routes)


@dataclass(frozen=True)
class ParseIssue:
    """Non-fatal or fatal issue encountered during parsing or extraction."""

    file: str
    message: str
    severity: Severity = Severity.WARNING
    line: int | None = None

    def sort_key(self) -> tuple[str, int, str]:
        return (self.file, self.line if self.line is not None else -1, self.message)


@dataclass(frozen=True)
class RepositoryIndex:
    """Ordered collection of module documents for rendering."""

    modules: tuple[ModuleDocument, ...] = ()

    def sort_key(self) -> tuple[object, ...]:
        """Deterministic key covering modules and nested collections."""
        return tuple(m.sort_key() for m in self.sorted_modules())

    def sorted_modules(self) -> tuple[ModuleDocument, ...]:
        return tuple(sorted(self.modules, key=lambda m: m.sort_key()))

    def with_sorted_collections(self) -> RepositoryIndex:
        """Return a copy with modules and nested collections sorted."""
        return RepositoryIndex(
            modules=tuple(m.with_sorted_collections() for m in self.sorted_modules())
        )


def build_placeholder_symbol(
    *,
    kind: SymbolKind,
    name: str,
    qualified_name: str,
    parameters: Sequence[ParameterDoc] = (),
    return_annotation: str | None = None,
    is_async: bool = False,
    decorators: Sequence[str] = (),
) -> SymbolDocument:
    """Build a placeholder symbol entry when no docstring is present (FR-017).

    The placeholder retains name, parameters, and return annotation so
    generated docs still describe the signature.
    """
    return SymbolDocument(
        kind=kind,
        name=name,
        qualified_name=qualified_name,
        docstring=None,
        parameters=tuple(parameters),
        return_annotation=return_annotation,
        is_async=is_async,
        decorators=tuple(decorators),
    )
