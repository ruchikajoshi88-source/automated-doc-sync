# Automated Documentation Sync — Design Review (v1 MVP)

## Document Information

| Field | Value |
| --- | --- |
| **Review Type** | Pre-implementation architecture & security review |
| **Reviewers** | Principal Software Engineer, Security Architect |
| **Documents Reviewed** | [requirements.md](./requirements.md), [architecture.md](./architecture.md) |
| **Review Date** | 2026-08-14 |
| **Outcome** | **Approved with adjustments** — proceed to implementation after architecture updates |

---

## 1. Executive Summary

The proposed layered pipeline architecture **aligns well** with MVP requirements: AST-only parsing, partial sync, Markdown output with custom-block preservation, CLI + pre-commit triggers, and modular separation of concerns.

This review identified **14 findings** across security, reliability, performance, and edge cases. **None are blockers** for MVP, but **9 require architectural adjustments** (documented in §6 and reflected in updated [architecture.md](./architecture.md)).

**Overall assessment:** The design is sound for v1. Agreed adjustments strengthen path sandboxing, config safety, merge determinism, stale-doc handling, and operational safety before code is written.

---

## 2. Review Methodology

Each finding is classified by:

| Dimension | Description |
| --- | --- |
| **Severity** | Critical / High / Medium / Low |
| **Category** | Security, Performance, Reliability, Requirements Gap, Operability |
| **Status** | Open → **Agreed** (mitigation accepted) / Deferred (post-MVP) |

Traceability to requirements uses IDs from [requirements.md](./requirements.md).

---

## 3. Requirements Coverage Assessment

| Area | Coverage | Notes |
| --- | --- | --- |
| CLI & pre-commit triggers | ✅ Complete | FR-001 – FR-004 |
| AST extraction | ✅ Complete | FR-010 – FR-018 |
| Markdown generation | ✅ Complete | FR-020 – FR-027 |
| Custom block preservation | ⚠️ Partial | Merge algorithm was underspecified; **slot-based IDs agreed** (DR-008) |
| Error handling | ⚠️ Partial | Merge/render failure taxonomy needed clarification (DR-009) |
| Configuration | ⚠️ Partial | YAML safety and path sandbox rules missing (DR-002, DR-003) |
| Performance (500 files / 30s) | ✅ Likely achievable | Guardrails added for large files and hook scope (DR-006, DR-012) |
| Security (NFR-020 – NFR-022) | ⚠️ Partial | Symlink, subprocess, and output-dir escape gaps (DR-001 – DR-004) |
| Deterministic output | ⚠️ Partial | Anchor collision and orphan docs unaddressed (DR-007, DR-010) |

---

## 4. Findings

### 4.1 Security

#### DR-001 — Symlink & path escape via output directory
| | |
| --- | --- |
| **Severity** | **High** |
| **Category** | Security |
| **Description** | `PathValidator` resolves canonical paths but the architecture did not define behavior for symlinks. A symlink inside `docs/` or a malicious `output_dir` config could redirect writes outside the intended sandbox on some platforms. |
| **Requirements** | NFR-011, NFR-022 |
| **Recommendation** | Reject symlinks for write targets; require `output_dir` to be a relative path resolved under `repo_root`; verify resolved path is prefixed by resolved `repo_root`. |
| **Status** | **Agreed** |

#### DR-002 — Unsafe YAML deserialization
| | |
| --- | --- |
| **Severity** | **High** |
| **Category** | Security |
| **Description** | PyYAML `load()` can execute arbitrary Python objects. Config files are project-controlled but may be merged from untrusted forks. |
| **Requirements** | NFR-020, NFR-021 |
| **Recommendation** | Mandate `yaml.safe_load()` only; reject unknown config keys; validate schema with strict types. |
| **Status** | **Agreed** |

#### DR-003 — Repository root CLI injection / traversal
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Security |
| **Description** | `--repo-root` accepts user input. Without normalization, `../` paths or UNC paths on Windows could scan unintended directories. |
| **Requirements** | NFR-011 |
| **Recommendation** | Resolve to absolute path at startup; optionally warn when repo root is outside cwd; never follow symlinks during scan (or resolve and validate membership). |
| **Status** | **Agreed** |

#### DR-004 — Git subprocess command injection
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Security |
| **Description** | `GitStager` runs shell commands. Filenames with metacharacters (e.g., `$(...)`) could be dangerous if `shell=True` is used. |
| **Requirements** | NFR-020 |
| **Recommendation** | Use `subprocess.run([...])` with argument lists only; `shell=False`; validate staged paths are under `output_dir`. |
| **Status** | **Agreed** |

#### DR-005 — Pre-commit hook overwrite without chaining
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Operability / Security |
| **Description** | Installing hook by overwriting `.git/hooks/pre-commit` silently removes existing hooks (lint, tests). |
| **Requirements** | FR-003 |
| **Recommendation** | Detect existing hook; chain by invoking previous hook after doc-sync; create timestamped backup; document manual merge path. |
| **Status** | **Agreed** |

---

### 4.2 Performance

#### DR-006 — Pre-commit runs full sync on every commit
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Performance / Operability |
| **Description** | Hook invokes full repository scan even when no `.py` files changed, violating spirit of NFR-001 for day-to-day dev flow. |
| **Requirements** | NFR-001, FR-003 |
| **Recommendation** | Default hook mode: sync only if staged files match `*.py` or config changed; `--full` flag forces complete scan. |
| **Status** | **Agreed** |

#### DR-007 — Unbounded file size and memory use
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Performance / Reliability |
| **Description** | Architecture loads entire source files and holds full `RepositoryIndex` in memory. A multi-MB `.py` file or generated docstring could cause excessive memory use or slow parse. |
| **Requirements** | NFR-001 |
| **Recommendation** | Enforce configurable `max_source_bytes` (default 1 MiB); skip with warning. Stream scanner; do not retain AST after extraction. |
| **Status** | **Agreed** |

#### DR-008 — Sequential processing acceptable but unmeasured
| | |
| --- | --- |
| **Severity** | **Low** |
| **Category** | Performance |
| **Description** | Sequential parse is fine for ~500 files but no benchmark harness defined. |
| **Requirements** | NFR-001 |
| **Recommendation** | Add integration perf test fixture (~500 files) in CI with soft timeout budget; defer parallelism post-MVP. |
| **Status** | **Agreed** |

---

### 4.3 Reliability & Edge Cases

#### DR-009 — Ambiguous blocking failure: merge vs render
| | |
| --- | --- |
| **Severity** | **High** |
| **Category** | Reliability / Requirements Gap |
| **Description** | FR-044 blocks commit on "formatting failures" but architecture did not classify custom-block merge corruption (unclosed markers, overlapping regions) as blocking. |
| **Requirements** | FR-042, FR-044 |
| **Recommendation** | Treat merge validation failures as **blocking** (`DocMergeError`); treat extraction warnings as non-blocking. Document exit-code mapping explicitly. |
| **Status** | **Agreed** |

#### DR-010 — Stale documentation for deleted/renamed modules
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Reliability |
| **Description** | Regeneration updates existing pages but never removes docs for deleted modules. TOC links rot; violates FR-023 spirit. |
| **Requirements** | FR-022, FR-023, FR-026 |
| **Recommendation** | Track generated file manifest per run; optionally prune orphaned docs under `docs/modules/` (config: `prune_orphans: true` default). Never prune files containing custom blocks unless `--force-prune`. |
| **Status** | **Agreed** |

#### DR-011 — Custom block merge positional ambiguity
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Reliability |
| **Description** | "Insert at original relative positions" is underspecified. Reordering generated sections breaks custom content placement across runs. |
| **Requirements** | FR-030, FR-031, NFR-012 |
| **Recommendation** | Require **named slot IDs** in custom markers: `<!-- custom:start intro -->`; merge by slot name, not byte offset. |
| **Status** | **Agreed** |

#### DR-012 — Dynamic route paths not extractable via AST
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Requirements Gap |
| **Description** | FastAPI/Flask routes using variables, f-strings, or computed prefixes cannot be statically resolved. Architecture implies full path extraction. |
| **Requirements** | FR-015, FR-016, FR-041 |
| **Recommendation** | Extract literal paths only; render dynamic expressions as `<dynamic>` with warning; document limitation in generated API.md footer. |
| **Status** | **Agreed** |

#### DR-013 — Encoding and non-UTF-8 source files
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Reliability |
| **Description** | No encoding policy. Python 3 defaults to UTF-8 but legacy files may use other encodings; `ast.parse` requires decodable source. |
| **Requirements** | FR-040, NFR-010 |
| **Recommendation** | Read as UTF-8 with strict decoding; on failure try `tokenize.detect_encoding`; skip file with warning if undecodable. |
| **Status** | **Agreed** |

#### DR-014 — Concurrent sync runs (race conditions)
| | |
| --- | --- |
| **Severity** | **Medium** |
| **Category** | Reliability |
| **Description** | Two simultaneous CLI runs can interleave atomic writes or corrupt manifest. |
| **Requirements** | NFR-013 |
| **Recommendation** | Acquire exclusive lock file `.doc-sync.lock` in output dir at run start; fail fast if lock held > stale threshold. |
| **Status** | **Agreed** |

---

### 4.4 Additional Edge Cases (Documented — No Architecture Change Required)

| Edge Case | Expected MVP Behavior |
| --- | --- |
| Empty `.py` file | Emit module page with "No public symbols" placeholder |
| File with syntax error mid-commit | Skip file; warn; partial sync (FR-040) |
| Duplicate symbol names in nested scopes | Document inner definitions with qualified anchors; dedupe anchors with suffix |
| `@property` / `@classmethod` / `@staticmethod` | Render as methods with decorator badges |
| Private symbols (`_name`) | Excluded by default; `include_private: false` config |
| Windows path length > 260 chars | Hash long module paths for filename: `modules/<hash>__<truncated>.md` with mapping in manifest |
| Manual edit inside `doc-sync:begin/end` region | Overwritten on next sync (by design per FR-026) |
| User removes custom `end` marker | **Blocking** merge error with line number |
| `API.md` custom blocks | Supported via same slot mechanism as module pages |
| Namespace packages (no `__init__.py`) | Supported; module path derived from file path |
| Type hints with forward refs / `from __future__ import annotations` | Render via `ast.unparse()` on annotation nodes |

---

## 5. Risk Register (Summary)

| ID | Risk | Severity | Likelihood | Mitigation | Residual Risk |
| --- | --- | --- | --- | --- | --- |
| R-01 | Write escape via symlinks | High | Low | Path sandbox + no symlink writes | Low |
| R-02 | YAML deserialization exploit | High | Low | `safe_load` + schema validation | Low |
| R-03 | Stale/orphan doc pages | Medium | High | Manifest + prune policy | Low |
| R-04 | Custom block merge data loss | Medium | Medium | Slot-based merge IDs | Low |
| R-05 | Dynamic route false docs | Medium | High | Literal-only + `<dynamic>` placeholder | Medium (accepted) |
| R-06 | Pre-commit dev friction | Medium | High | Staged-file incremental sync | Low |
| R-07 | Concurrent run corruption | Medium | Low | Lock file | Low |
| R-08 | Anchor collisions | Low | Medium | Dedup suffix algorithm | Low |
| R-09 | AST limitations vs libCST | Low | Medium | Document known gaps; defer libCST | Medium (accepted) |

---

## 6. Agreed Design Decisions

The following decisions are **binding for v1 implementation**:

| # | Decision | Rationale |
| --- | --- | --- |
| **DD-01** | **Strict output sandbox** — all writes must resolve under `{repo_root}/{output_dir}`; symlinks rejected for write paths | Closes DR-001 |
| **DD-02** | **`yaml.safe_load` only** with explicit schema validation | Closes DR-002 |
| **DD-03** | **Slot-based custom blocks** — `<!-- custom:start <slot-id> -->` required; merge by slot ID | Closes DR-011 |
| **DD-04** | **Merge failures are blocking**; extraction failures are non-blocking | Closes DR-009; aligns FR-043/FR-044 |
| **DD-05** | **Orphan doc pruning enabled by default** with custom-block safety guard | Closes DR-010 |
| **DD-06** | **Pre-commit incremental mode** — sync when staged `*.py` or config differs | Closes DR-006 |
| **DD-07** | **Git subprocess hardening** — list args, no shell, path-validated staging | Closes DR-004 |
| **DD-08** | **Hook chaining with backup** on install | Closes DR-005 |
| **DD-09** | **Run lock file** `.doc-sync.lock` with 5-minute stale TTL | Closes DR-014 |
| **DD-10** | **Source file limits** — default 1 MiB max; UTF-8 with encoding detection fallback | Closes DR-007, DR-013 |
| **DD-11** | **Route paths: literals only**; dynamic values rendered as `<dynamic>` | Closes DR-012 |
| **DD-12** | **Private symbols excluded** by default (`include_private: false`) | Reduces noise; configurable |
| **DD-13** | **Long filename hashing** on Windows for path > 200 chars | Prevents write failures |
| **DD-14** | **`pathspec` included as required dependency** for gitignore-compatible excludes | Resolves open decision; FR-011 |

---

## 7. Deferred Items (Post-MVP)

| Item | Reason |
| --- | --- |
| Parallel file parsing | Premature; benchmark first |
| libCST for comment-preserving parse | Out of scope per requirements |
| OpenAPI export | Out of scope |
| Intelligent diff-based merge | Complexity; slot model sufficient for v1 |
| File watcher / on-save sync | Out of scope |
| Docstring format normalization (Google/NumPy) | Out of scope |

---

## 8. Pre-Implementation Checklist

Before writing production code, implementation MUST include:

- [ ] `PathValidator` with sandbox, symlink, and Windows path-length rules (DD-01, DD-13)
- [ ] `ConfigLoader` using `yaml.safe_load` and strict schema (DD-02)
- [ ] `CustomBlockMerger` with slot IDs and blocking validation (DD-03, DD-04)
- [ ] `StaleDocManager` with manifest and prune guard (DD-05)
- [ ] Hook incremental mode and hook chaining installer (DD-06, DD-08)
- [ ] `GitStager` subprocess hardening (DD-07)
- [ ] `RunLock` context manager (DD-09)
- [ ] Source size and encoding guards in `AstParser` (DD-10)
- [ ] Route extractor literal-only policy with warnings (DD-11)
- [ ] Unit tests for each agreed decision
- [ ] Integration test for orphan pruning and merge failure paths

---

## 9. Sign-Off

| Role | Assessment |
| --- | --- |
| **Principal Software Engineer** | Architecture is implementable and requirement-aligned after agreed adjustments. Proceed. |
| **Security Architect** | Residual risks acceptable for offline CLI MVP with DD-01 – DD-10 enforced. |

**Next step:** Implement per updated [architecture.md](./architecture.md).
