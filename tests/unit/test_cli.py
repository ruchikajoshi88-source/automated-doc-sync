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


def test_sync_not_implemented_message() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["sync"])
    assert result.exit_code != 0
    assert "not yet implemented" in result.output.lower() or "Phase 5" in result.output
