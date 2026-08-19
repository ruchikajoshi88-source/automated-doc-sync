"""Unit tests for CLI entry point."""

from click.testing import CliRunner

from doc_sync.entrypoints.cli import main


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Sync Python docstrings" in result.output
    assert "sync" in result.output
    assert "install-hook" in result.output


def test_sync_help_documents_incremental_and_full() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["sync", "--help"])
    assert result.exit_code == 0
    assert "--incremental" in result.output
    assert "--full" in result.output
    assert "--stage" in result.output


def test_sync_rejects_incremental_and_full_together() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["sync", "--incremental", "--full"])
    assert result.exit_code != 0
    assert "--incremental and --full" in result.output


def test_sync_not_implemented_message() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["sync"])
    assert result.exit_code != 0
    assert "not yet implemented" in result.output.lower()
    assert "Phase 5" not in result.output
