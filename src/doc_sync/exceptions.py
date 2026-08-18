"""Shared exception hierarchy and process exit codes."""

from __future__ import annotations

from enum import Enum


EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_PARTIAL = 2


class Severity(str, Enum):
    """Issue severity for parse and sync reporting."""

    WARNING = "warning"
    ERROR = "error"


class DocSyncError(Exception):
    """Base exception for all doc-sync errors."""


class ConfigError(DocSyncError):
    """Invalid or unsafe configuration."""


class PathValidationError(DocSyncError):
    """Path traversal, symlink, or sandbox violation."""


class DocMergeError(DocSyncError):
    """Custom block merge validation failure (blocking)."""


class DocWriteError(DocSyncError):
    """Documentation file write failure (blocking)."""


class RunLockError(DocSyncError):
    """Concurrent sync lock held by another process (blocking)."""
