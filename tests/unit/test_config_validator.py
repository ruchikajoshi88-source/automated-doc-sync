"""Unit tests for configuration validation."""

from pathlib import Path

import pytest

from doc_sync.config.schema import DocSyncConfig
from doc_sync.config.validator import validate_config
from doc_sync.exceptions import ConfigError


def test_validate_config_normalizes_repo_root(tmp_path: Path) -> None:
    config = DocSyncConfig(repo_root=tmp_path, output_dir="docs")
    validated = validate_config(config)
    assert validated.repo_root == tmp_path.resolve()


def test_validate_config_rejects_absolute_output_dir(tmp_path: Path) -> None:
    config = DocSyncConfig(repo_root=tmp_path, output_dir=str(tmp_path / "docs"))
    with pytest.raises(ConfigError, match="relative"):
        validate_config(config)


def test_validate_config_rejects_zero_max_source_bytes(tmp_path: Path) -> None:
    config = DocSyncConfig(repo_root=tmp_path, max_source_bytes=0)
    with pytest.raises(ConfigError, match="max_source_bytes"):
        validate_config(config)


def test_validate_config_rejects_missing_repo_root(tmp_path: Path) -> None:
    missing = tmp_path / "missing"
    config = DocSyncConfig(repo_root=missing)
    with pytest.raises(ConfigError, match="not a directory"):
        validate_config(config)


def test_validate_config_rejects_empty_include(tmp_path: Path) -> None:
    config = DocSyncConfig(repo_root=tmp_path, include=())
    with pytest.raises(ConfigError, match="include"):
        validate_config(config)
