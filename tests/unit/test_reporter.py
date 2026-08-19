"""Unit tests for SyncReporter exit-code mapping."""

from doc_sync.core.reporter import SyncReporter
from doc_sync.exceptions import EXIT_FAILURE, EXIT_PARTIAL, EXIT_SUCCESS, DocWriteError
from doc_sync.models.documents import ParseIssue


def test_reporter_success_exit_code() -> None:
    result = SyncReporter().build_summary()
    assert result.exit_code == EXIT_SUCCESS
    assert result.warning_count == 0


def test_reporter_partial_exit_code_when_warnings() -> None:
    reporter = SyncReporter()
    reporter.record_warning(ParseIssue(file="app.py", message="skipped"))
    result = reporter.build_summary()
    assert result.exit_code == EXIT_PARTIAL
    assert result.warning_count == 1


def test_reporter_failure_exit_code_on_blocking_error() -> None:
    reporter = SyncReporter()
    reporter.record_warning(ParseIssue(file="app.py", message="skipped"))
    reporter.record_blocking_error(DocWriteError("write failed"))
    result = reporter.build_summary()
    assert result.exit_code == EXIT_FAILURE
    assert reporter.blocking_error is not None


def test_reporter_emit_summary_includes_blocking_error(capsys) -> None:
    reporter = SyncReporter()
    reporter.record_blocking_error(DocWriteError("cannot write API.md"))
    result = reporter.build_summary()
    reporter.emit_summary(result)
    err = capsys.readouterr().err
    assert "processed=" in err
    assert "cannot write API.md" in err
