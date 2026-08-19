"""Git staging of generated documentation via subprocess (list args, no shell)."""

from __future__ import annotations

from pathlib import Path


class GitStager:
    """Stages generated documentation paths via subprocess (Phase 6 — T-025)."""

    def __init__(self, repo_root: Path) -> None:
        self._repo_root = repo_root

    def stage(self, paths: list[Path]) -> None:
        """Run `git add` on validated paths under the documentation output directory."""
        raise NotImplementedError("GitStager.stage is implemented in Phase 6 (T-025)")
