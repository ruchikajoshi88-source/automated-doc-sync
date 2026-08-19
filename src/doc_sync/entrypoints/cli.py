"""Command-line interface for doc-sync."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

import click

from doc_sync import __version__
from doc_sync.config.loader import ConfigLoader
from doc_sync.config.schema import DocSyncConfig
from doc_sync.config.validator import validate_config
from doc_sync.core.sync_engine import SyncEngine
from doc_sync.exceptions import DocSyncError


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
    help="Optional path to .doc-sync.yaml.",
)
@click.option("--stage", is_flag=True, help="Stage generated docs in Git after sync.")
@click.option(
    "--force-prune",
    is_flag=True,
    help="Remove orphan docs even when custom blocks are present.",
)
@click.option(
    "--incremental",
    is_flag=True,
    default=False,
    help="Only sync when staged .py or config files changed (hook mode).",
)
@click.option(
    "--full",
    is_flag=True,
    default=False,
    help="Force a complete repository scan.",
)
def sync(
    repo_root: Path,
    config_path: Path | None,
    stage: bool,
    force_prune: bool,
    incremental: bool,
    full: bool,
) -> None:
    """
    Run a documentation sync against the repository.

    Examples:

      doc-sync sync

      doc-sync sync --repo-root /path/to/project --stage
    """
    if incremental and full:
        raise click.UsageError("--incremental and --full cannot be used together.")

    scan_full = not incremental
    try:
        config = _load_runtime_config(repo_root, config_path, stage=stage)
        engine = SyncEngine(config)
        result = engine.run(
            stage=stage or config.stage_on_sync,
            force_prune=force_prune,
            full=scan_full,
        )
        raise SystemExit(result.exit_code)
    except NotImplementedError as exc:
        raise click.ClickException(
            "Documentation sync is not yet implemented. "
            "Install succeeded; the pipeline will land in a later release."
        ) from exc
    except DocSyncError as exc:
        raise click.ClickException(str(exc)) from exc


def _load_runtime_config(
    repo_root: Path,
    config_path: Path | None,
    *,
    stage: bool,
) -> DocSyncConfig:
    """Resolve config from --config / discovered file, then apply CLI overrides."""
    loader = ConfigLoader(repo_root)
    overrides: dict[str, Any] = {}
    if stage:
        overrides["stage_on_sync"] = True
    try:
        if config_path is not None:
            config = loader.load_from_path(config_path, overrides)
        else:
            config = loader.load(overrides)
    except NotImplementedError:
        config = DocSyncConfig.defaults(repo_root)
        if stage:
            config = replace(config, stage_on_sync=True)
    return validate_config(config)


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

    Backs up and chains any existing pre-commit hook.
    """
    from doc_sync.git.hook_installer import HookInstaller

    try:
        HookInstaller(repo_root).install()
    except NotImplementedError as exc:
        raise click.ClickException(
            "Git hook installation is not yet implemented."
        ) from exc
    except DocSyncError as exc:
        raise click.ClickException(str(exc)) from exc


if __name__ == "__main__":
    main()
