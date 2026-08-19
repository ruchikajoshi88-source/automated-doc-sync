"""Unit tests for domain models."""

from dataclasses import FrozenInstanceError

import pytest

from doc_sync.exceptions import Severity
from doc_sync.models.documents import (
    ModuleDocument,
    ParameterDoc,
    ParameterKind,
    ParseIssue,
    RepositoryIndex,
    RouteDocument,
    RouteFramework,
    SymbolDocument,
    SymbolKind,
    build_placeholder_symbol,
)


def test_placeholder_symbol_marks_missing_docstring() -> None:
    symbol = build_placeholder_symbol(
        kind=SymbolKind.FUNCTION,
        name="fetch_user",
        qualified_name="app.services.fetch_user",
        parameters=(ParameterDoc(name="user_id", annotation="int"),),
        return_annotation="User | None",
        is_async=True,
    )
    assert symbol.is_placeholder
    assert symbol.docstring is None
    assert symbol.name == "fetch_user"
    assert symbol.parameters[0].annotation == "int"
    assert symbol.return_annotation == "User | None"
    assert symbol.is_async is True


def test_repository_index_sort_key_is_deterministic() -> None:
    modules = (
        ModuleDocument(module_path="b.mod", source_relpath="b/mod.py"),
        ModuleDocument(module_path="a.mod", source_relpath="a/mod.py"),
    )
    index_a = RepositoryIndex(modules=modules)
    index_b = RepositoryIndex(modules=tuple(reversed(modules)))
    assert index_a.sort_key() == index_b.sort_key()
    assert [key[0] for key in index_a.sort_key()] == ["a.mod", "b.mod"]


def test_identical_inputs_produce_identical_sort_keys() -> None:
    def build() -> RepositoryIndex:
        return RepositoryIndex(
            modules=(
                ModuleDocument(
                    module_path="app.api",
                    source_relpath="app/api.py",
                    symbols=(
                        SymbolDocument(
                            kind=SymbolKind.FUNCTION,
                            name="run",
                            qualified_name="app.api.run",
                            parameters=(ParameterDoc(name="x", annotation="int"),),
                        ),
                    ),
                    routes=(
                        RouteDocument(
                            framework=RouteFramework.FLASK,
                            methods=("GET",),
                            path="/health",
                            handler_name="health",
                        ),
                    ),
                ),
            )
        )

    assert build().sort_key() == build().sort_key()
    assert build() == build()


def test_nested_collections_sort_deterministically() -> None:
    module = ModuleDocument(
        module_path="app.api",
        source_relpath="app/api.py",
        symbols=(
            SymbolDocument(
                kind=SymbolKind.CLASS,
                name="Zeta",
                qualified_name="app.api.Zeta",
            ),
            SymbolDocument(
                kind=SymbolKind.CLASS,
                name="Alpha",
                qualified_name="app.api.Alpha",
            ),
        ),
        routes=(
            RouteDocument(
                framework=RouteFramework.FASTAPI,
                methods=("POST",),
                path="/b",
                handler_name="b_handler",
            ),
            RouteDocument(
                framework=RouteFramework.FASTAPI,
                methods=("GET",),
                path="/a",
                handler_name="a_handler",
            ),
        ),
    )
    assert [s.name for s in module.sorted_symbols] == ["Alpha", "Zeta"]
    assert [r.path for r in module.sorted_routes] == ["/a", "/b"]

    sorted_module = module.with_sorted_collections()
    assert [s.name for s in sorted_module.symbols] == ["Alpha", "Zeta"]
    assert [r.path for r in sorted_module.routes] == ["/a", "/b"]
    assert [s.name for s in module.symbols] == ["Zeta", "Alpha"]


def test_models_are_frozen() -> None:
    symbol = SymbolDocument(
        kind=SymbolKind.FUNCTION,
        name="run",
        qualified_name="app.run",
    )
    with pytest.raises((AttributeError, FrozenInstanceError)):
        symbol.name = "other"  # type: ignore[misc]


def test_parameter_kind_default() -> None:
    param = ParameterDoc(name="x")
    assert param.kind == ParameterKind.POSITIONAL_OR_KEYWORD


def test_parse_issue_defaults_to_warning() -> None:
    issue = ParseIssue(file="app.py", message="syntax error", line=3)
    assert issue.severity == Severity.WARNING
    assert issue.sort_key() == ("app.py", 3, "syntax error")
