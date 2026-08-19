"""Git pre-commit hook wrapper (Phase 6 — T-027)."""

from __future__ import annotations

import sys

from doc_sync.exceptions import EXIT_FAILURE


def main() -> None:
    """Entry point invoked by the installed pre-commit hook.

    Intended policy: merge/write/lock failures return exit code 1 (block
    commit); extraction warnings must not block the commit.
    """
    raise NotImplementedError("Pre-commit hook wrapper is not yet implemented.")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError:
        print("doc-sync hook: not yet implemented", file=sys.stderr)
        sys.exit(EXIT_FAILURE)
