"""Output-path sandbox: traversal rejection, symlink checks, long-name hashing."""

from __future__ import annotations

from pathlib import Path

from doc_sync.config.schema import DocSyncConfig


class PathValidator:
    """Validates paths against the output sandbox (Phase 2 — T-007)."""

    def __init__(self, config: DocSyncConfig) -> None:
        self._config = config

    def resolve_output_path(self, module_path: str) -> Path:
        """Map a qualified module path to a Markdown file under output_dir."""
        raise NotImplementedError(
            "PathValidator.resolve_output_path is implemented in Phase 2 (T-007)"
        )

    def validate_write_path(self, path: Path) -> Path:
        """Ensure a write target resolves strictly under {repo_root}/{output_dir}."""
        raise NotImplementedError(
            "PathValidator.validate_write_path is implemented in Phase 2 (T-007)"
        )
