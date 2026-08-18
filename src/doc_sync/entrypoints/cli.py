"""Command-line interface for doc-sync."""

from __future__ import annotations

from pathlib import Path

import click

from doc_sync import __version__
from doc_sync.config.schema import DocSyncConfig
from doc_sync.config.validator import validate_config
from doc_sync.core.sync_engine import SyncEngine
from doc_sync.exceptions import (
    EXIT_FAILURE,
    DocSyncError,
)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="doc-sync")
def main() -> None:
    """Sync Python docstrings and API routes to Markdown documentation."""


@main.command("sync")
@click.option(
    "--repo-root",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=".",
    show_default=True,
    help="Repository root to scan.",
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
    help="Optional path to .doc-sync.yaml (Phase 2).",
)
@click.option("--stage", is_flag=True, help="Stage generated docs in Git after sync.")
@click.option(
    "--force-prune",
    is_flag=True,
    help="Remove orphan docs even when custom blocks are present.",
)
@click.option(
    "--full",
    is_flag=True,
    default=True,
    show_default=True,
    help="Scan entire repository (default).",
)
def sync(
    repo_root: Path,
    config_path: Path | None,
    stage: bool,
    force_prune: bool,
    full: bool,
) -> None:
    """
    Run a documentation sync against the repository.

    Examples:

      doc-sync sync

      doc-sync sync --repo-root /path/to/project --stage
    """
    _ = config_path  # wired in Phase 2 (T-005)
    try:
        config = validate_config(DocSyncConfig.defaults(repo_root))
        engine = SyncEngine(config)
        result = engine.run(stage=stage, force_prune=force_prune, full=full)
        raise SystemExit(result.exit_code)
    except NotImplementedError as exc:
        raise click.ClickException(
            "Sync pipeline is not yet implemented (Phase 5). "
            "Phase 1 scaffold: project structure and core types are in place."
        ) from exc
    except DocSyncError as exc:
        raise click.ClickException(str(exc)) from exc


@main.command("install-hook")
@click.option(
    "--repo-root",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=".",
    show_default=True,
    help="Repository root containing .git directory.",
)
def install_hook(repo_root: Path) -> None:
    """
    Install a Git pre-commit hook that runs doc-sync.

    Backs up and chains any existing pre-commit hook (Phase 6 — T-026).
    """
    from doc_sync.git.hook_installer import HookInstaller

    _ = repo_root
    try:
        HookInstaller(repo_root).install()
    except NotImplementedError as exc:
        raise click.ClickException(
            "Hook installation is not yet implemented (Phase 6)."
        ) from exc
    except DocSyncError as exc:
        raise click.ClickException(str(exc)) from exc


if __name__ == "__main__":
    main()
