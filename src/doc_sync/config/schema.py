"""Configuration schema and defaults."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_OUTPUT_DIR = "docs"
DEFAULT_MAX_SOURCE_BYTES = 1_048_576  # 1 MiB
DEFAULT_CUSTOM_BLOCK_START = "<!-- custom:start"
DEFAULT_CUSTOM_BLOCK_END = "<!-- custom:end"
DEFAULT_INCLUDE = ("**/*.py",)
DEFAULT_EXCLUDE = (
    ".git/**",
    "venv/**",
    ".venv/**",
    "__pycache__/**",
    "*.egg-info/**",
    "dist/**",
    "build/**",
)


@dataclass(frozen=True)
class CustomBlockMarkers:
    """Delimiter strings for manually authored Markdown regions."""

    start: str = DEFAULT_CUSTOM_BLOCK_START
    end: str = DEFAULT_CUSTOM_BLOCK_END


@dataclass(frozen=True)
class DocSyncConfig:
    """Validated runtime configuration for a documentation sync run."""

    repo_root: Path
    output_dir: str = DEFAULT_OUTPUT_DIR
    include: tuple[str, ...] = DEFAULT_INCLUDE
    exclude: tuple[str, ...] = DEFAULT_EXCLUDE
    custom_block_markers: CustomBlockMarkers = field(default_factory=CustomBlockMarkers)
    stage_on_sync: bool = False
    prune_orphans: bool = True
    include_private: bool = False
    max_source_bytes: int = DEFAULT_MAX_SOURCE_BYTES

    @property
    def output_path(self) -> Path:
        """Absolute path to the documentation output directory."""
        return self.repo_root / self.output_dir

    @classmethod
    def defaults(cls, repo_root: Path | str) -> DocSyncConfig:
        """Build a config instance using default values for the given repo root."""
        return cls(repo_root=Path(repo_root).resolve())
