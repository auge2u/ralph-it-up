# Phase 1 — Hardening the Core: Design

**Date:** 2026-02-26
**Status:** Approved
**Scope:** Automated test suite, CI workflow, error handling improvements, expanded quality gates

## Objective

Make the existing plugin production-ready with robust validation, automated quality assurance, and clear error messages. Done when CI blocks PRs on gate failure and all gate types have automated tests.

## Decisions

- **Test framework (Python):** pytest with `tmp_path` fixtures — best fit for file-based validation logic
- **Test framework (bash):** bats-core — industry standard for bash testing; CI installs via `apt-get`
- **Bash script testing:** subprocess via bats, not Python subprocess — cleaner isolation
- **Test location:** co-located under plugin (`plugins/ralph-it-up-roadmap/tests/`) — consistent with self-contained plugin principle
- **CI triggers:** push to `main` + all PRs
- **CI jobs:** two parallel jobs (python-tests, bash-tests)

## Test Organization

```
plugins/ralph-it-up-roadmap/
  tests/
    python/
      conftest.py                  # shared fixtures (scopecraft dir builders via tmp_path)
      test_file_count.py           # _check_file_count gate
      test_pattern_count.py        # _check_pattern_count gate
      test_pattern_exists.py       # _check_pattern_exists gate
      test_min_lines.py            # _check_min_lines gate
      test_integration.py          # full validate_all() runs (passing + broken fixtures)
    bash/
      test_validate_gates.bats     # all 6 gates + 2 new gates, --json/--quiet modes, error paths
      helpers/
        setup_scopecraft.bash      # helper to build fixture dirs in $BATS_TEST_TMPDIR
  requirements-dev.txt             # pytest, pytest-cov
```

Fixtures are built programmatically — no checked-in fixture files.

## CI Workflow

**File:** `.github/workflows/validate.yml`
**Triggers:** `push` to `main`, `pull_request`

```yaml
jobs:
  python-tests:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - setup Python 3.11
      - pip install -r plugins/ralph-it-up-roadmap/requirements-dev.txt
      - pytest plugins/ralph-it-up-roadmap/tests/python/ -v --tb=short

  bash-tests:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - apt-get install bats shellcheck
      - shellcheck plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh
      - bats plugins/ralph-it-up-roadmap/tests/bash/
```

Jobs run in parallel. No caching (install time <15s).

## Error Handling Improvements

**Python validator (`validate_quality_gates.py`):**
- Add `encoding="utf-8"` to all file opens in `_check_min_lines`, `_check_pattern_exists`, `_check_pattern_count`
- Improve PyYAML fallback message: `"PyYAML not installed — using built-in gates. Install with: pip install pyyaml"`

**Bash validator (`validate-gates-handler.sh`):**
- Add bash version check at top (requires bash 4+ for `declare -A`):
  ```bash
  if [[ "${BASH_VERSINFO[0]}" -lt 4 ]]; then
    echo "Error: bash 4+ required (found $BASH_VERSION). On macOS: brew install bash" >&2
    exit 1
  fi
  ```
- Improve "no scopecraft dir" error: append `"Run a roadmap command first to generate outputs"`

## Expanded Quality Gates

Two new gates added to both validators:

| Gate | Check | Requirement |
|------|-------|-------------|
| `roadmap_has_content` | `min_lines` | `ROADMAP.md` ≥ 50 lines |
| `open_questions_populated` | `pattern_count` | `OPEN_QUESTIONS.md` has ≥ 1 `## ` section header |

**Rationale:**
- `roadmap_has_content` — catches stub outputs where phase headers exist but phases are empty; uses the existing `_check_min_lines` infrastructure (currently unused by any default gate)
- `open_questions_populated` — no gate currently validates the *content* of `OPEN_QUESTIONS.md`, only its existence

Both gates need implementation in Python (`DEFAULT_GATES`) and bash (`validate-gates-handler.sh`), plus tests in both test suites.

## Definition of Done

- All 8 quality gates have automated tests (Python + bash)
- CI runs in <60 seconds
- CI blocks PRs when any gate fails
- `shellcheck` passes on the bash validator
- Zero manual validation steps required for contribution
