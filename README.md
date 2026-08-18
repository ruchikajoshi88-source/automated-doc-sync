# Automated Documentation Sync

Sync Python docstrings, type hints, and FastAPI/Flask route annotations to structured Markdown documentation.

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```bash
doc-sync --help
doc-sync sync --repo-root .
doc-sync install-hook
```

See [requirements.md](./requirements.md), [architecture.md](./architecture.md), and [impl-plan.md](./impl-plan.md) for design documentation.
