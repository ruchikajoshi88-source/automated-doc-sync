"""Unit tests for configuration schema."""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from doc_sync.config.schema import (
    DEFAULT_MAX_SOURCE_BYTES,
    DEFAULT_OUTPUT_DIR,
    CustomBlockMarkers,
    DocSyncConfig,
)


def test_default_config_values(tmp_path: Path) -> None:
    config = DocSyncConfig.defaults(tmp_path)
    assert config.output_dir == DEFAULT_OUTPUT_DIR
    assert config.prune_orphans is True
    assert config.include_private is False
    assert config.max_source_bytes == DEFAULT_MAX_SOURCE_BYTES
    assert config.stage_on_sync is False
    assert config.include == ("**/*.py",)
    assert ".git/**" in config.exclude
    assert "venv/**" in config.exclude
    assert isinstance(config.custom_block_markers, CustomBlockMarkers)


def test_output_path_resolution(tmp_path: Path) -> None:
    config = DocSyncConfig.defaults(tmp_path)
    assert config.output_path == tmp_path.resolve() / "docs"


def test_custom_config_values(tmp_path: Path) -> None:
    config = DocSyncConfig(
        repo_root=tmp_path,
        output_dir="documentation",
        stage_on_sync=True,
        include_private=True,
        include=("src/**/*.py",),
        exclude=("tests/**",),
        max_source_bytes=2048,
    )
    assert config.output_dir == "documentation"
    assert config.stage_on_sync is True
    assert config.include_private is True
    assert config.include == ("src/**/*.py",)
    assert config.exclude == ("tests/**",)
    assert config.max_source_bytes == 2048


def test_config_is_frozen(tmp_path: Path) -> None:
    config = DocSyncConfig.defaults(tmp_path)
    with pytest.raises((AttributeError, FrozenInstanceError)):
        config.output_dir = "other"  # type: ignore[misc]


def test_custom_block_markers_include_slot_and_closing(tmp_path: Path) -> None:
    markers = DocSyncConfig.defaults(tmp_path).custom_block_markers
    assert markers.start_tag("intro") == "<!-- custom:start intro -->"
    assert markers.end_tag("intro") == "<!-- custom:end intro -->"


def test_custom_block_slot_id_rejects_whitespace() -> None:
    markers = CustomBlockMarkers()
    with pytest.raises(ValueError, match="slot_id"):
        markers.start_tag("intro notes")
