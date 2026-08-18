"""Git staging and pre-commit hook installation (Phase 6 — T-025–T-026)."""

from __future__ import annotations

from pathlib import Path


class GitStager:
    """Stages generated documentation paths via subprocess (Phase 6 — T-025)."""

    def __init__(self, repo_root: Path) -> None:
        self._repo_root = repo_root

    def stage(self, paths: list[Path]) -> None:
        raise NotImplementedError("GitStager.stage is implemented in Phase 6 (T-025)")


class HookInstaller:
    """Installs and chains Git pre-commit hooks (Phase 6 — T-026)."""

    def __init__(self, repo_root: Path) -> None:
        self._repo_root = Path(repo_root).resolve()

    def install(self) -> None:
        raise NotImplementedError("HookInstaller.install is implemented in Phase 6 (T-026)")
