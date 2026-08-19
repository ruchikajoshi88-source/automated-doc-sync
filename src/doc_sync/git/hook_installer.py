"""Pre-commit hook installation with backup and chaining."""

from __future__ import annotations

from pathlib import Path


class HookInstaller:
    """Installs and chains Git pre-commit hooks (Phase 6 — T-026)."""

    def __init__(self, repo_root: Path) -> None:
        self._repo_root = Path(repo_root).resolve()

    def install(self) -> None:
        """Write `.git/hooks/pre-commit`, backing up and chaining any existing hook."""
        raise NotImplementedError("HookInstaller.install is implemented in Phase 6 (T-026)")
