"""Unit tests for configuration schema."""

from pathlib import Path

from doc_sync.config.schema import (
    DEFAULT_MAX_SOURCE_BYTES,
    DEFAULT_OUTPUT_DIR,
    DocSyncConfig,
)


def test_default_config_values(tmp_path: Path) -> None:
    config = DocSyncConfig.defaults(tmp_path)
    assert config.output_dir == DEFAULT_OUTPUT_DIR
    assert config.prune_orphans is True
    assert config.include_private is False
    assert config.max_source_bytes == DEFAULT_MAX_SOURCE_BYTES
    assert config.stage_on_sync is False
    assert "**/*.py" in config.include
    assert ".git/**" in config.exclude


def test_output_path_resolution(tmp_path: Path) -> None:
    config = DocSyncConfig.defaults(tmp_path)
    assert config.output_path == tmp_path.resolve() / "docs"


def test_custom_config_values(tmp_path: Path) -> None:
    config = DocSyncConfig(
        repo_root=tmp_path,
        output_dir="documentation",
        stage_on_sync=True,
        include_private=True,
    )
    assert config.output_dir == "documentation"
    assert config.stage_on_sync is True
    assert config.include_private is True
