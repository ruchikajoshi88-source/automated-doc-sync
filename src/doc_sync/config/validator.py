"""Configuration validation rules (Phase 2 — T-006)."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from doc_sync.config.schema import CustomBlockMarkers, DocSyncConfig
from doc_sync.exceptions import ConfigError


def validate_config(config: DocSyncConfig) -> DocSyncConfig:
    """
    Validate and normalize a DocSyncConfig instance.

    Enforces relative in-repo output_dir, positive max_source_bytes, and absolute repo_root.
    """
    repo_root = Path(config.repo_root).resolve()
    if not repo_root.is_dir():
        raise ConfigError(f"repo_root is not a directory: {repo_root}")

    _validate_output_dir(config.output_dir, repo_root)
    _validate_custom_block_markers(config.custom_block_markers)

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

    return replace(config, repo_root=repo_root)


def _validate_output_dir(output_dir: str, repo_root: Path) -> None:
    """Reject absolute paths and any output_dir that escapes repo_root (NFR-011)."""
    if not output_dir or not output_dir.strip():
        raise ConfigError("output_dir must be a non-empty relative path")

    candidate = Path(output_dir)
    if candidate.is_absolute():
        raise ConfigError("output_dir must be a relative path")

    if ".." in candidate.parts:
        raise ConfigError("output_dir must not contain '..' segments")

    resolved = (repo_root / candidate).resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ConfigError("output_dir must resolve inside repo_root") from exc


def _validate_custom_block_markers(markers: CustomBlockMarkers) -> None:
    if not markers.start.strip() or not markers.end.strip():
        raise ConfigError("custom_block_markers start and end must be non-empty")
    if markers.start == markers.end:
        raise ConfigError("custom_block_markers start and end must differ")
