"""Configuration validation rules (Phase 2 — T-006)."""

from __future__ import annotations

from pathlib import Path

from doc_sync.config.schema import DocSyncConfig
from doc_sync.exceptions import ConfigError


def validate_config(config: DocSyncConfig) -> DocSyncConfig:
    """
    Validate and normalize a DocSyncConfig instance.

    Enforces relative output_dir, positive max_source_bytes, and absolute repo_root.
    """
    repo_root = Path(config.repo_root).resolve()
    if not repo_root.is_dir():
        raise ConfigError(f"repo_root is not a directory: {repo_root}")

    if Path(config.output_dir).is_absolute():
        raise ConfigError("output_dir must be a relative path")

    if config.max_source_bytes <= 0:
        raise ConfigError("max_source_bytes must be greater than zero")

    if not config.include:
        raise ConfigError("include patterns must not be empty")

    if not config.exclude:
        raise ConfigError("exclude patterns must not be empty")

    if not all(isinstance(p, str) and p for p in config.include):
        raise ConfigError("include patterns must be non-empty strings")

    if not all(isinstance(p, str) and p for p in config.exclude):
        raise ConfigError("exclude patterns must be non-empty strings")

    return DocSyncConfig(
        repo_root=repo_root,
        output_dir=config.output_dir,
        include=config.include,
        exclude=config.exclude,
        custom_block_markers=config.custom_block_markers,
        stage_on_sync=config.stage_on_sync,
        prune_orphans=config.prune_orphans,
        include_private=config.include_private,
        max_source_bytes=config.max_source_bytes,
    )
