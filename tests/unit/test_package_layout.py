"""Verify package layout matches architecture.md §12."""

from pathlib import Path

import doc_sync

REQUIRED_RELATIVE_PATHS = (
    "entrypoints/cli.py",
    "entrypoints/hook.py",
    "core/sync_engine.py",
    "core/reporter.py",
    "config/loader.py",
    "config/schema.py",
    "config/validator.py",
    "scanner/repository_scanner.py",
    "parser/ast_parser.py",
    "extractors/base.py",
    "extractors/module.py",
    "extractors/symbols.py",
    "extractors/fastapi_routes.py",
    "extractors/flask_routes.py",
    "models/documents.py",
    "renderer/anchors.py",
    "renderer/markdown_renderer.py",
    "renderer/toc_builder.py",
    "renderer/custom_block_merger.py",
    "io/doc_writer.py",
    "io/path_validator.py",
    "io/stale_doc_manager.py",
    "io/run_lock.py",
    "git/stager.py",
    "git/hook_installer.py",
    "exceptions.py",
    "interfaces.py",
)


def test_architecture_package_layout_exists() -> None:
    package_root = Path(doc_sync.__file__).resolve().parent
    missing = [rel for rel in REQUIRED_RELATIVE_PATHS if not (package_root / rel).is_file()]
    assert missing == []
