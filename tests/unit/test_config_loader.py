"""Unit tests for ConfigLoader discovery helpers."""

from pathlib import Path

import pytest

from doc_sync.config.loader import ConfigLoader, load_config
from doc_sync.exceptions import ConfigError


def test_discover_config_path_when_present(tmp_path: Path) -> None:
    config_file = tmp_path / ".doc-sync.yaml"
    config_file.write_text("output_dir: docs\n", encoding="utf-8")
    loader = ConfigLoader(tmp_path)
    assert loader.discover_config_path() == config_file.resolve()


def test_discover_config_path_when_missing(tmp_path: Path) -> None:
    loader = ConfigLoader(tmp_path)
    assert loader.discover_config_path() is None


def test_discover_pyproject_path(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    loader = ConfigLoader(tmp_path)
    assert loader.discover_pyproject_path() == pyproject.resolve()


def test_resolve_config_source_prefers_explicit_path(tmp_path: Path) -> None:
    explicit = tmp_path / "custom.yaml"
    explicit.write_text("output_dir: docs\n", encoding="utf-8")
    (tmp_path / ".doc-sync.yaml").write_text("output_dir: other\n", encoding="utf-8")
    loader = ConfigLoader(tmp_path)
    assert loader.resolve_config_source(explicit) == explicit


def test_load_config_wrapper_maps_not_implemented(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not yet implemented"):
        load_config(tmp_path)
