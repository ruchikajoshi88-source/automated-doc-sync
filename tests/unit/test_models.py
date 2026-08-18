"""Unit tests for domain models."""

from pathlib import Path

from doc_sync.models.documents import (
    ModuleDocument,
    ParameterDoc,
    ParameterKind,
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
    assert index_a.sort_key() == index_b.sort_key() == ("a.mod", "b.mod")


def test_module_document_sorted_symbols_and_routes() -> None:
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


def test_models_are_frozen() -> None:
    symbol = SymbolDocument(
        kind=SymbolKind.FUNCTION,
        name="run",
        qualified_name="app.run",
    )
    try:
        symbol.name = "other"  # type: ignore[misc]
        raised = False
    except AttributeError:
        raised = True
    assert raised


def test_parameter_kind_default() -> None:
    param = ParameterDoc(name="x")
    assert param.kind == ParameterKind.POSITIONAL_OR_KEYWORD
