"""Unit tests for exception hierarchy and exit codes."""

import pytest

from doc_sync.exceptions import (
    EXIT_FAILURE,
    EXIT_PARTIAL,
    EXIT_SUCCESS,
    ConfigError,
    DocMergeError,
    DocSyncError,
    DocWriteError,
    PathValidationError,
    RunLockError,
    Severity,
)


@pytest.mark.parametrize(
    ("exc_type",),
    [
        (ConfigError,),
        (PathValidationError,),
        (DocMergeError,),
        (DocWriteError,),
        (RunLockError,),
    ],
)
def test_exceptions_inherit_from_doc_sync_error(exc_type: type[DocSyncError]) -> None:
    assert issubclass(exc_type, DocSyncError)
    assert issubclass(exc_type, Exception)


def test_exit_codes_match_architecture() -> None:
    assert EXIT_SUCCESS == 0
    assert EXIT_FAILURE == 1
    assert EXIT_PARTIAL == 2


def test_severity_values() -> None:
    assert Severity.WARNING.value == "warning"
    assert Severity.ERROR.value == "error"


def test_doc_sync_error_is_raised_as_base() -> None:
    with pytest.raises(DocSyncError):
        raise ConfigError("bad config")
