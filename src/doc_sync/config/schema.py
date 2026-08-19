"""Configuration schema and defaults.

Field types and defaults (architecture §5.3, T-004):

* ``repo_root``: ``Path`` — repository root (normalized to absolute by validator)
* ``output_dir``: ``str`` — relative output directory (default ``"docs"``)
* ``include``: ``tuple[str, ...]`` — gitignore-style include globs (default ``("**/*.py",)``)
* ``exclude``: ``tuple[str, ...]`` — gitignore-style exclude globs (venv, .git, caches)
* ``custom_block_markers``: ``CustomBlockMarkers`` — slot delimiter prefixes (``<!-- custom:start <id> -->``)
* ``stage_on_sync``: ``bool`` — stage generated files after sync (default ``False``)
* ``prune_orphans``: ``bool`` — remove stale module docs (default ``True``)
* ``include_private``: ``bool`` — document ``_prefixed`` symbols (default ``False``)
* ``max_source_bytes``: ``int`` — skip oversized sources (default ``1_048_576`` / 1 MiB)
"""

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
    """Delimiter prefixes for slot-based custom Markdown regions (DD-03).

    Slot tags are assembled as ``f"{start} {slot_id} -->"`` /
    ``f"{end} {slot_id} -->"``, matching ``<!-- custom:start intro -->``.
    """

    start: str = DEFAULT_CUSTOM_BLOCK_START
    end: str = DEFAULT_CUSTOM_BLOCK_END

    def start_tag(self, slot_id: str) -> str:
        """Return the opening marker for ``slot_id`` (FR-030)."""
        return f"{self.start} {_require_slot_id(slot_id)} -->"

    def end_tag(self, slot_id: str) -> str:
        """Return the closing marker for ``slot_id`` (FR-030)."""
        return f"{self.end} {_require_slot_id(slot_id)} -->"


def _require_slot_id(slot_id: str) -> str:
    if not slot_id or any(ch.isspace() for ch in slot_id):
        raise ValueError("custom block slot_id must be a non-empty token without whitespace")
    return slot_id


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
