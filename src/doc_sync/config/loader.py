"""Configuration file loading (Phase 2 — T-005)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from doc_sync.config.schema import DocSyncConfig
from doc_sync.exceptions import ConfigError


class ConfigLoader:
    """Loads and merges project configuration from YAML, TOML, and CLI overrides."""

    CONFIG_FILENAME = ".doc-sync.yaml"
    PYPROJECT_FILENAME = "pyproject.toml"
    TOOL_SECTION = "doc-sync"

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root).resolve()

    def load(self, cli_overrides: Mapping[str, Any] | None = None) -> DocSyncConfig:
        """Load configuration with precedence: defaults < file < CLI overrides."""
        raise NotImplementedError(
            "YAML/TOML configuration loading is not yet implemented. "
            "Use DocSyncConfig.defaults(repo_root) until the loader lands."
        )

    def load_from_path(
        self,
        config_path: Path,
        cli_overrides: Mapping[str, Any] | None = None,
    ) -> DocSyncConfig:
        """Load configuration from an explicit YAML path, then apply CLI overrides."""
        raise NotImplementedError(
            "YAML/TOML configuration loading is not yet implemented. "
            "Use DocSyncConfig.defaults(repo_root) until the loader lands."
        )

    def discover_config_path(self) -> Path | None:
        """Return path to `.doc-sync.yaml` if present in repo root."""
        candidate = self.repo_root / self.CONFIG_FILENAME
        return candidate if candidate.is_file() else None

    def discover_pyproject_path(self) -> Path | None:
        """Return path to `pyproject.toml` if present in repo root."""
        candidate = self.repo_root / self.PYPROJECT_FILENAME
        return candidate if candidate.is_file() else None

    def resolve_config_source(self, config_path: Path | None = None) -> Path | None:
        """Return the explicit config path, else a discovered `.doc-sync.yaml`."""
        if config_path is not None:
            return Path(config_path)
        return self.discover_config_path()


def load_config(repo_root: Path | str, **cli_overrides: Any) -> DocSyncConfig:
    """Convenience wrapper for ConfigLoader.load."""
    loader = ConfigLoader(repo_root)
    try:
        return loader.load(cli_overrides or {})
    except NotImplementedError as exc:
        raise ConfigError(
            "Configuration file loading is not yet implemented. "
            "Use DocSyncConfig.defaults(repo_root) until the YAML/TOML loader lands."
        ) from exc
