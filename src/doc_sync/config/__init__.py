"""Configuration loading and validation."""

from doc_sync.config.loader import ConfigLoader, load_config
from doc_sync.config.schema import (
    DEFAULT_EXCLUDE,
    DEFAULT_INCLUDE,
    DEFAULT_MAX_SOURCE_BYTES,
    DEFAULT_OUTPUT_DIR,
    CustomBlockMarkers,
    DocSyncConfig,
)
from doc_sync.config.validator import validate_config

__all__ = [
    "ConfigLoader",
    "CustomBlockMarkers",
    "DEFAULT_EXCLUDE",
    "DEFAULT_INCLUDE",
    "DEFAULT_MAX_SOURCE_BYTES",
    "DEFAULT_OUTPUT_DIR",
    "DocSyncConfig",
    "load_config",
    "validate_config",
]
