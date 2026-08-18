"""Configuration loading and validation."""

from doc_sync.config.schema import (
    DEFAULT_EXCLUDE,
    DEFAULT_INCLUDE,
    DEFAULT_MAX_SOURCE_BYTES,
    DEFAULT_OUTPUT_DIR,
    CustomBlockMarkers,
    DocSyncConfig,
)

__all__ = [
    "CustomBlockMarkers",
    "DEFAULT_EXCLUDE",
    "DEFAULT_INCLUDE",
    "DEFAULT_MAX_SOURCE_BYTES",
    "DEFAULT_OUTPUT_DIR",
    "DocSyncConfig",
]
