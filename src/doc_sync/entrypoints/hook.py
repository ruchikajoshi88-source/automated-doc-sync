"""Git pre-commit hook wrapper (Phase 6 — T-027)."""

from __future__ import annotations

import sys

from doc_sync.exceptions import EXIT_FAILURE


def main() -> None:
    """Entry point invoked by the installed pre-commit hook."""
    raise NotImplementedError("Pre-commit hook wrapper is implemented in Phase 6 (T-027)")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError:
        print("doc-sync hook: not yet implemented (Phase 6)", file=sys.stderr)
        sys.exit(EXIT_FAILURE)
