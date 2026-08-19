"""Unit tests for extractor and renderer protocol contracts."""

from pathlib import Path

from doc_sync.config.schema import DocSyncConfig
from doc_sync.extractors.base import RouteExtractorBase
from doc_sync.extractors.fastapi_routes import FastAPIRouteExtractor
from doc_sync.extractors.flask_routes import FlaskRouteExtractor
from doc_sync.extractors.module import ModuleExtractor
from doc_sync.extractors.symbols import SymbolExtractor
from doc_sync.interfaces import (
    ModuleExtractorProtocol,
    OutputRenderer,
    RouteExtractor,
    SymbolExtractorProtocol,
)
from doc_sync.models.documents import ParseIssue
from doc_sync.renderer.markdown_renderer import MarkdownRenderer


def test_route_extractors_satisfy_protocol() -> None:
    assert isinstance(FastAPIRouteExtractor(), RouteExtractor)
    assert isinstance(FlaskRouteExtractor(), RouteExtractor)


def test_module_and_symbol_extractors_satisfy_protocols(tmp_path: Path) -> None:
    config = DocSyncConfig.defaults(tmp_path)
    assert isinstance(ModuleExtractor(), ModuleExtractorProtocol)
    assert isinstance(SymbolExtractor(config), SymbolExtractorProtocol)


def test_markdown_renderer_satisfies_output_renderer(tmp_path: Path) -> None:
    config = DocSyncConfig.defaults(tmp_path)
    assert isinstance(MarkdownRenderer(config), OutputRenderer)


def test_route_extractor_base_collects_warnings() -> None:
    extractor = RouteExtractorBase()
    extractor._warn(ParseIssue(file="app.py", message="dynamic path"))
    assert len(extractor.warnings()) == 1
    extractor._reset_warnings()
    assert extractor.warnings() == ()
