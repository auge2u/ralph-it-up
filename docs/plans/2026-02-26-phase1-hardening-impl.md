# Phase 1 — Hardening the Core: Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a full test suite (pytest + bats), GitHub Actions CI, error handling fixes, and two new quality gates to the ralph-it-up-roadmap plugin.

**Architecture:** Tests live co-located at `plugins/ralph-it-up-roadmap/tests/` split into `python/` (pytest) and `bash/` (bats). TDD order: write failing test → verify fail → implement → verify pass → commit. New gates added to both validators simultaneously.

**Tech Stack:** Python 3.11+, pytest, bats-core, shellcheck, GitHub Actions

---

### Task 1: Create test infrastructure

**Files:**
- Create: `plugins/ralph-it-up-roadmap/requirements-dev.txt`
- Create: `plugins/ralph-it-up-roadmap/tests/python/conftest.py`
- Create: `plugins/ralph-it-up-roadmap/tests/bash/helpers/setup_scopecraft.bash`

**Step 1: Create requirements-dev.txt**

```
pytest>=7.0
pytest-cov
```

**Step 2: Create conftest.py with shared fixtures**

```python
# plugins/ralph-it-up-roadmap/tests/python/conftest.py
import sys
from pathlib import Path

import pytest

# Make validate_quality_gates importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "hooks"))

# ── Fixture content constants ──────────────────────────────────────────────────

PASSING_ROADMAP = """\
# Roadmap

## Phase 1 — Foundation

**Objective:** Establish core infrastructure.

**Customer Value:** Users can run the plugin end-to-end.

**Deliverables:**
- Core validation logic
- Basic test coverage

**Metrics / KRs:**
- All gates pass on first run

---

## Phase 2 — Growth

**Objective:** Expand coverage and improve reliability.

**Customer Value:** Users trust outputs are complete.

**Deliverables:**
- Extended quality gates
- CI integration

**Metrics / KRs:**
- CI runs in under 60 seconds

---

## Phase 3 — Scale

**Objective:** Support community contributions.

**Customer Value:** External contributors can add plugins.

**Deliverables:**
- Plugin contribution guide
- Automated submission validation

**Metrics / KRs:**
- 3+ plugins in marketplace

---
"""

PASSING_EPICS = """\
# Epics and Stories

## Epic 1: Core Validation

### Story 1.1: Gate validation runs

**Acceptance Criteria**
- [ ] All 6 gates execute without error
- [ ] Exit codes are correct

### Story 1.2: Missing file handling

**Acceptance Criteria**
- [ ] Missing files produce clear error messages
- [ ] Validator does not crash

## Epic 2: CI Integration

### Story 2.1: PR gate enforcement

**Acceptance Criteria**
- [ ] CI blocks merge when gates fail
- [ ] CI passes when all gates pass

### Story 2.2: Parallel jobs

**Acceptance Criteria**
- [ ] Python tests run in parallel with bash tests
- [ ] Total CI time under 60 seconds

## Epic 3: Documentation

### Story 3.1: Contributor guide

**Acceptance Criteria**
- [ ] New contributor can add plugin without assistance
- [ ] All required files documented
"""

PASSING_RISKS = """\
# Risks and Dependencies

| Risk | Type | Likelihood | Impact | Mitigation |
|------|------|------------|--------|------------|
| Test flakiness with file I/O | Technical | Medium | High | Use deterministic fixtures |
| CI setup complexity | Technical | Low | Medium | Start minimal, expand later |
| Low community adoption | GTM | Medium | High | Active outreach |
| Documentation drift | Product | Medium | Medium | Generate from source |
"""

PASSING_METRICS = """\
# Metrics and PMF

## North Star Metric

**Metric:** Time-to-first-roadmap for a new user

**Target:** Under 5 minutes

## Supporting Metrics

- CI run time < 60 seconds
- 100% of quality gates have automated tests
"""

PASSING_OPEN_QUESTIONS = """\
# Open Questions

## Question 1: Hosting for documentation site

Should we use GitHub Pages or an external service?

## Question 2: Analytics opt-in mechanism

How do we surface the analytics opt-in to users?
"""


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def passing_scopecraft(tmp_path):
    """Complete scopecraft directory that passes all gates."""
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "VISION_AND_STAGE_DEFINITION.md").write_text("# Vision\n\nContent.\n", encoding="utf-8")
    (sc / "ROADMAP.md").write_text(PASSING_ROADMAP, encoding="utf-8")
    (sc / "EPICS_AND_STORIES.md").write_text(PASSING_EPICS, encoding="utf-8")
    (sc / "RISKS_AND_DEPENDENCIES.md").write_text(PASSING_RISKS, encoding="utf-8")
    (sc / "METRICS_AND_PMF.md").write_text(PASSING_METRICS, encoding="utf-8")
    (sc / "OPEN_QUESTIONS.md").write_text(PASSING_OPEN_QUESTIONS, encoding="utf-8")
    return tmp_path


@pytest.fixture
def empty_scopecraft(tmp_path):
    """Empty scopecraft directory."""
    (tmp_path / "scopecraft").mkdir()
    return tmp_path


@pytest.fixture
def no_scopecraft(tmp_path):
    """Base dir with no scopecraft directory at all."""
    return tmp_path
```

**Step 3: Create bats helper**

```bash
# plugins/ralph-it-up-roadmap/tests/bash/helpers/setup_scopecraft.bash
# Source this in bats tests: source "$BATS_TEST_DIRNAME/helpers/setup_scopecraft.bash"

HOOK="$BATS_TEST_DIRNAME/../../hooks/validate-gates-handler.sh"

setup_passing_scopecraft() {
  local dir="$1"
  mkdir -p "$dir/scopecraft"

  cat > "$dir/scopecraft/VISION_AND_STAGE_DEFINITION.md" <<'EOF'
# Vision

Content.
EOF

  # ROADMAP.md: 3 phases, >= 50 lines
  python3 - "$dir/scopecraft/ROADMAP.md" <<'PYEOF'
import sys
lines = ["# Roadmap\n\n"]
for i in range(1, 4):
    lines.append(f"## Phase {i} — Phase Title\n\n")
    lines.extend(["Content line.\n"] * 15)
    lines.append("\n---\n\n")
with open(sys.argv[1], "w") as f:
    f.writelines(lines)
PYEOF

  cat > "$dir/scopecraft/EPICS_AND_STORIES.md" <<'EOF'
# Epics

## Epic 1

### Story 1
**Acceptance Criteria**
- [ ] criterion

### Story 2
**Acceptance Criteria**
- [ ] criterion

### Story 3
**Acceptance Criteria**
- [ ] criterion

### Story 4
**Acceptance Criteria**
- [ ] criterion

### Story 5
**Acceptance Criteria**
- [ ] criterion
EOF

  cat > "$dir/scopecraft/RISKS_AND_DEPENDENCIES.md" <<'EOF'
| Risk | Type | Notes |
|------|------|-------|
| Risk 1 | Technical | note |
| Risk 2 | Product | note |
| Risk 3 | GTM | note |
EOF

  cat > "$dir/scopecraft/METRICS_AND_PMF.md" <<'EOF'
# Metrics

## North Star Metric

Time-to-first-roadmap.
EOF

  cat > "$dir/scopecraft/OPEN_QUESTIONS.md" <<'EOF'
# Open Questions

## Question 1

Details here.
EOF
}
```

**Step 4: Verify pytest can find tests**

```bash
cd /path/to/ralph-it-up
pip install -r plugins/ralph-it-up-roadmap/requirements-dev.txt
pytest plugins/ralph-it-up-roadmap/tests/python/ --collect-only
```

Expected: `no tests ran` (no test files yet, but no import errors)

**Step 5: Commit**

```bash
git add plugins/ralph-it-up-roadmap/requirements-dev.txt \
        plugins/ralph-it-up-roadmap/tests/
git commit -m "test: add test infrastructure (conftest, bats helper, requirements-dev)"
```

---

### Task 2: Python tests — `_check_file_count`

**Files:**
- Create: `plugins/ralph-it-up-roadmap/tests/python/test_file_count.py`

**Step 1: Write tests**

```python
# plugins/ralph-it-up-roadmap/tests/python/test_file_count.py
from pathlib import Path
from validate_quality_gates import QualityGateValidator

GATE = {
    "id": "all_outputs_exist",
    "name": "All required outputs exist",
    "check": "file_count",
    "path": "scopecraft/*.md",
    "expect": 6,
    "severity": "blocker",
}


def test_file_count_passes_with_exactly_six(passing_scopecraft):
    v = QualityGateValidator(passing_scopecraft, [GATE])
    result = v.validate_all()[0]
    assert result.passed is True
    assert result.actual == 6


def test_file_count_fails_with_five_files(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    for i in range(5):
        (sc / f"file{i}.md").write_text("content")
    v = QualityGateValidator(tmp_path, [GATE])
    result = v.validate_all()[0]
    assert result.passed is False
    assert result.actual == 5


def test_file_count_fails_with_empty_dir(empty_scopecraft):
    v = QualityGateValidator(empty_scopecraft, [GATE])
    result = v.validate_all()[0]
    assert result.passed is False
    assert result.actual == 0


def test_file_count_fails_with_seven_files(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    for i in range(7):
        (sc / f"file{i}.md").write_text("content")
    v = QualityGateValidator(tmp_path, [GATE])
    result = v.validate_all()[0]
    assert result.passed is False
    assert result.actual == 7


def test_file_count_result_has_expected_set(passing_scopecraft):
    v = QualityGateValidator(passing_scopecraft, [GATE])
    result = v.validate_all()[0]
    assert result.expected == "6"
```

**Step 2: Run tests**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_file_count.py -v
```

Expected: all PASS (the implementation already exists)

**Step 3: Commit**

```bash
git add plugins/ralph-it-up-roadmap/tests/python/test_file_count.py
git commit -m "test: add _check_file_count tests"
```

---

### Task 3: Python tests — `_check_pattern_count`

**Files:**
- Create: `plugins/ralph-it-up-roadmap/tests/python/test_pattern_count.py`

**Step 1: Write tests**

```python
# plugins/ralph-it-up-roadmap/tests/python/test_pattern_count.py
import pytest
from validate_quality_gates import QualityGateValidator


def make_gate(path, pattern, min=None, max=None):
    g = {"id": "test_gate", "name": "Test", "check": "pattern_count",
         "path": path, "pattern": pattern, "severity": "blocker"}
    if min is not None:
        g["min"] = min
    if max is not None:
        g["max"] = max
    return g


def test_pattern_count_passes_at_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n## Phase 2\n## Phase 3\n")
    gate = make_gate("scopecraft/ROADMAP.md", r"^## Phase \d", min=3)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True
    assert result.actual == 3


def test_pattern_count_fails_below_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n## Phase 2\n")
    gate = make_gate("scopecraft/ROADMAP.md", r"^## Phase \d", min=3)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 2


def test_pattern_count_fails_above_maximum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("[TODO]\n[TODO]\n")
    gate = make_gate("scopecraft/ROADMAP.md", r"\[TODO\]", max=0)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 2


def test_pattern_count_passes_at_zero_when_max_zero(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "file.md").write_text("No placeholders here.\n")
    gate = make_gate("scopecraft/file.md", r"\[TODO\]", max=0)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True
    assert result.actual == 0


def test_pattern_count_fails_when_no_files_found(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    gate = make_gate("scopecraft/NONEXISTENT.md", r"## Phase", min=1)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert "No files found" in result.message


def test_pattern_count_aggregates_across_glob(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "a.md").write_text("[TODO]\n")
    (sc / "b.md").write_text("[TODO]\n[TODO]\n")
    gate = make_gate("scopecraft/*.md", r"\[TODO\]", max=0)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 3
```

**Step 2: Run tests**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_pattern_count.py -v
```

Expected: all PASS

**Step 3: Commit**

```bash
git add plugins/ralph-it-up-roadmap/tests/python/test_pattern_count.py
git commit -m "test: add _check_pattern_count tests"
```

---

### Task 4: Python tests — `_check_pattern_exists` and `_check_min_lines`

**Files:**
- Create: `plugins/ralph-it-up-roadmap/tests/python/test_pattern_exists.py`
- Create: `plugins/ralph-it-up-roadmap/tests/python/test_min_lines.py`

**Step 1: Write pattern_exists tests**

```python
# plugins/ralph-it-up-roadmap/tests/python/test_pattern_exists.py
from validate_quality_gates import QualityGateValidator


def make_gate(path, pattern):
    return {"id": "test", "name": "Test", "check": "pattern_exists",
            "path": path, "pattern": pattern, "severity": "blocker"}


def test_pattern_exists_passes_when_found(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "METRICS_AND_PMF.md").write_text("## North Star Metric\n\nContent.\n")
    gate = make_gate("scopecraft/METRICS_AND_PMF.md", r"North Star Metric")
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True


def test_pattern_exists_fails_when_not_found(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "METRICS_AND_PMF.md").write_text("## Some Other Section\n")
    gate = make_gate("scopecraft/METRICS_AND_PMF.md", r"North Star Metric")
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False


def test_pattern_exists_fails_when_file_missing(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    gate = make_gate("scopecraft/MISSING.md", r"North Star Metric")
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert "not found" in result.message
```

**Step 2: Write min_lines tests**

```python
# plugins/ralph-it-up-roadmap/tests/python/test_min_lines.py
from validate_quality_gates import QualityGateValidator


def make_gate(path, min_lines):
    return {"id": "test", "name": "Test", "check": "min_lines",
            "path": path, "min": min_lines, "severity": "blocker"}


def test_min_lines_passes_at_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("\n" * 49 + "line 50\n")
    gate = make_gate("scopecraft/ROADMAP.md", 50)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True
    assert result.actual == 50


def test_min_lines_fails_below_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("short\n")
    gate = make_gate("scopecraft/ROADMAP.md", 50)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 1


def test_min_lines_fails_when_file_missing(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    gate = make_gate("scopecraft/MISSING.md", 50)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert "not found" in result.message
```

**Step 3: Run both**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_pattern_exists.py \
       plugins/ralph-it-up-roadmap/tests/python/test_min_lines.py -v
```

Expected: all PASS

**Step 4: Commit**

```bash
git add plugins/ralph-it-up-roadmap/tests/python/test_pattern_exists.py \
        plugins/ralph-it-up-roadmap/tests/python/test_min_lines.py
git commit -m "test: add _check_pattern_exists and _check_min_lines tests"
```

---

### Task 5: Python integration tests

**Files:**
- Create: `plugins/ralph-it-up-roadmap/tests/python/test_integration.py`

**Step 1: Write tests**

```python
# plugins/ralph-it-up-roadmap/tests/python/test_integration.py
from validate_quality_gates import QualityGateValidator


def test_all_gates_pass_on_complete_output(passing_scopecraft):
    v = QualityGateValidator(passing_scopecraft)
    results = v.validate_all()
    failed = [r for r in results if not r.passed]
    assert failed == [], f"Expected all gates to pass, failed: {[r.gate_id for r in failed]}"


def test_all_outputs_exist_gate_fails_on_empty_dir(empty_scopecraft):
    v = QualityGateValidator(empty_scopecraft)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["all_outputs_exist"].passed is False


def test_no_todo_gate_fails_when_placeholder_present(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n[TODO] fill this in\n")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["no_todo_placeholders"].passed is False


def test_unknown_check_type_returns_failed_result(tmp_path):
    gate = {"id": "bad", "name": "Bad", "check": "nonexistent_type",
            "path": "scopecraft/*.md", "severity": "blocker"}
    v = QualityGateValidator(tmp_path, [gate])
    result = v.validate_all()[0]
    assert result.passed is False
    assert "Unknown check type" in result.message
```

**Step 2: Run**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_integration.py -v
```

Expected: all PASS

**Step 3: Commit**

```bash
git add plugins/ralph-it-up-roadmap/tests/python/test_integration.py
git commit -m "test: add integration tests for validate_all()"
```

---

### Task 6: Error handling — Python encoding and message fixes

**Files:**
- Modify: `plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py`

**Step 1: Write failing test for encoding**

Add to `test_integration.py`:

```python
def test_validator_handles_unicode_content(tmp_path):
    """Validator should not crash on files with unicode characters."""
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "METRICS_AND_PMF.md").write_text(
        "## North Star Metric\n\nCafé → Success ✓\n", encoding="utf-8"
    )
    gate = {"id": "metrics_defined", "name": "North Star Metric",
            "check": "pattern_exists", "path": "scopecraft/METRICS_AND_PMF.md",
            "pattern": "North Star Metric", "severity": "blocker"}
    v = QualityGateValidator(tmp_path, [gate])
    result = v.validate_all()[0]
    assert result.passed is True  # Should not raise UnicodeDecodeError
```

**Step 2: Run — verify test passes (defensive test)**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_integration.py::test_validator_handles_unicode_content -v
```

Expected: PASS (this is a defensive test; the fix prevents future regression)

**Step 3: Fix encoding in validator**

In `plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py`, find every `open(` call and add `encoding="utf-8"`:

- `_check_min_lines` line ~167: `open(file_path, "r")` → `open(file_path, "r", encoding="utf-8")`
- `_check_pattern_count` line ~201: `open(file_path, "r")` → `open(file_path, "r", encoding="utf-8")`
- `_check_pattern_exists` line ~247: `open(file_path, "r")` → `open(file_path, "r", encoding="utf-8")`
- `load_gates_from_config` line ~270: `open(config_path, "r")` → `open(config_path, "r", encoding="utf-8")`
- `main()` scratchpad write line ~386: `open(scratchpad_path, "a")` → `open(scratchpad_path, "a", encoding="utf-8")`

**Step 4: Fix PyYAML fallback message**

Find (line ~27):
```python
    print("Warning: PyYAML not installed, using default gates", file=sys.stderr)
```
Replace with:
```python
    print("Warning: PyYAML not installed — using built-in gates. Install with: pip install pyyaml", file=sys.stderr)
```

**Step 5: Run all tests**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/ -v
```

Expected: all PASS

**Step 6: Commit**

```bash
git add plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py \
        plugins/ralph-it-up-roadmap/tests/python/test_integration.py
git commit -m "fix: add utf-8 encoding to all file opens, improve PyYAML fallback message"
```

---

### Task 7: New Python gate — `roadmap_has_content`

**Files:**
- Modify: `plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py`
- Create: `plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py`

**Step 1: Write failing test**

```python
# plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py
from validate_quality_gates import QualityGateValidator


def test_roadmap_has_content_passes_with_fifty_lines(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("\n" * 49 + "line 50\n", encoding="utf-8")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["roadmap_has_content"].passed is True


def test_roadmap_has_content_fails_with_stub(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n## Phase 2\n## Phase 3\n", encoding="utf-8")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["roadmap_has_content"].passed is False
```

**Step 2: Run — verify FAIL**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py::test_roadmap_has_content_passes_with_fifty_lines -v
```

Expected: FAIL with `KeyError: 'roadmap_has_content'` (gate doesn't exist yet)

**Step 3: Add gate to DEFAULT_GATES**

In `validate_quality_gates.py`, append to `DEFAULT_GATES` list (after the last existing gate):

```python
        {
            "id": "roadmap_has_content",
            "name": "Roadmap has substantive content",
            "check": "min_lines",
            "path": "scopecraft/ROADMAP.md",
            "min": 50,
            "severity": "blocker"
        },
```

**Step 4: Run — verify PASS**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py -v
```

Expected: PASS

**Step 5: Run full suite to check no regressions**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/ -v
```

Note: `test_all_gates_pass_on_complete_output` in `test_integration.py` must also pass — verify the `passing_scopecraft` fixture's `ROADMAP.md` content has ≥ 50 lines. It does (PASSING_ROADMAP in conftest.py is ~50+ lines). If it fails, pad PASSING_ROADMAP in `conftest.py`.

**Step 6: Commit**

```bash
git add plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py \
        plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py
git commit -m "feat: add roadmap_has_content quality gate (min 50 lines)"
```

---

### Task 8: New Python gate — `open_questions_populated`

**Files:**
- Modify: `plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py`
- Modify: `plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py`

**Step 1: Write failing test**

Append to `test_new_gates.py`:

```python
def test_open_questions_populated_passes_with_section(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "OPEN_QUESTIONS.md").write_text(
        "# Open Questions\n\n## Question 1\n\nDetails.\n", encoding="utf-8"
    )
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["open_questions_populated"].passed is True


def test_open_questions_populated_fails_with_empty_file(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "OPEN_QUESTIONS.md").write_text("# Open Questions\n", encoding="utf-8")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["open_questions_populated"].passed is False


def test_open_questions_populated_fails_when_file_missing(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["open_questions_populated"].passed is False
```

**Step 2: Run — verify FAIL**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py::test_open_questions_populated_passes_with_section -v
```

Expected: FAIL with `KeyError: 'open_questions_populated'`

**Step 3: Add gate to DEFAULT_GATES**

Append after `roadmap_has_content`:

```python
        {
            "id": "open_questions_populated",
            "name": "Open questions has at least one question",
            "check": "pattern_count",
            "path": "scopecraft/OPEN_QUESTIONS.md",
            "pattern": r"^## ",
            "min": 1,
            "severity": "blocker"
        },
```

**Step 4: Run — verify all new gate tests PASS**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py -v
```

**Step 5: Run full suite**

```bash
pytest plugins/ralph-it-up-roadmap/tests/python/ -v
```

Expected: all PASS

**Step 6: Commit**

```bash
git add plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py \
        plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py
git commit -m "feat: add open_questions_populated quality gate (min 1 section)"
```

---

### Task 9: Error handling — bash validator fixes

**Files:**
- Modify: `plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh`

**Step 1: Add bash version check**

After `set -euo pipefail`, insert:

```bash
# Require bash 4+ for associative arrays (declare -A)
if [[ "${BASH_VERSINFO[0]}" -lt 4 ]]; then
  echo "Error: bash 4+ required (found $BASH_VERSION). On macOS: brew install bash" >&2
  exit 1
fi
```

**Step 2: Improve "no scopecraft dir" error message**

Find:
```bash
    echo "Error: scopecraft directory not found at $SCOPECRAFT_DIR" >&2
```
Replace with:
```bash
    echo "Error: scopecraft directory not found at $SCOPECRAFT_DIR. Run a roadmap command first to generate outputs." >&2
```

**Step 3: Run shellcheck**

```bash
shellcheck plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh
```

Expected: no warnings or errors

**Step 4: Commit**

```bash
git add plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh
git commit -m "fix: add bash 4+ version check, improve no-scopecraft error message"
```

---

### Task 10: New bash gates — `roadmap_has_content` and `open_questions_populated`

**Files:**
- Modify: `plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh`

**Step 1: Add `roadmap_has_content` gate**

After the last existing gate block (Gate 6: no_todo_placeholders), append:

```bash
# Gate 7: roadmap_has_content (ROADMAP.md >= 50 lines)
if [[ -f "$roadmap_file" ]]; then
  line_count=$(wc -l < "$roadmap_file" | tr -d ' ')
  if [[ "$line_count" -ge 50 ]]; then
    gates[roadmap_has_content]="PASS"
    gate_details[roadmap_has_content]="$line_count lines"
  else
    gates[roadmap_has_content]="FAIL"
    gate_details[roadmap_has_content]="Expected >=50, found $line_count"
    all_passed=false
  fi
else
  gates[roadmap_has_content]="FAIL"
  gate_details[roadmap_has_content]="ROADMAP.md not found"
  all_passed=false
fi

# Gate 8: open_questions_populated (OPEN_QUESTIONS.md has >= 1 '## ' header)
open_questions_file="$SCOPECRAFT_DIR/OPEN_QUESTIONS.md"
if [[ -f "$open_questions_file" ]]; then
  oq_count=$(grep -cE "^## " "$open_questions_file" 2>/dev/null || echo 0)
  if [[ "$oq_count" -ge 1 ]]; then
    gates[open_questions_populated]="PASS"
    gate_details[open_questions_populated]="$oq_count questions"
  else
    gates[open_questions_populated]="FAIL"
    gate_details[open_questions_populated]="Expected >=1, found $oq_count"
    all_passed=false
  fi
else
  gates[open_questions_populated]="FAIL"
  gate_details[open_questions_populated]="OPEN_QUESTIONS.md not found"
  all_passed=false
fi
```

**Step 2: Update the gate list in the human-readable output loop**

Find:
```bash
    for gate in all_outputs_exist phases_in_range stories_have_acceptance_criteria risks_documented metrics_defined no_todo_placeholders; do
```
Replace with:
```bash
    for gate in all_outputs_exist phases_in_range stories_have_acceptance_criteria risks_documented metrics_defined no_todo_placeholders roadmap_has_content open_questions_populated; do
```

**Step 3: Update the total count in output**

Find:
```bash
    echo "Total: 6 | Passed: $passed_count | Failed: $failed_count"
```
Replace with:
```bash
    echo "Total: 8 | Passed: $passed_count | Failed: $failed_count"
```

**Step 4: Update JSON output block** to include the two new gates:

```bash
    "roadmap_has_content": { "passed": $([ "${gates[roadmap_has_content]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[roadmap_has_content]}" },
    "open_questions_populated": { "passed": $([ "${gates[open_questions_populated]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[open_questions_populated]}" }
```

(Remove the trailing comma from the previous last gate in the JSON block)

**Step 5: Run shellcheck**

```bash
shellcheck plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh
```

Expected: no warnings

**Step 6: Commit**

```bash
git add plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh
git commit -m "feat: add roadmap_has_content and open_questions_populated gates to bash validator"
```

---

### Task 11: Bats tests — all gates

**Files:**
- Create: `plugins/ralph-it-up-roadmap/tests/bash/test_validate_gates.bats`

**Step 1: Write bats test file**

```bash
#!/usr/bin/env bats
# plugins/ralph-it-up-roadmap/tests/bash/test_validate_gates.bats

load "helpers/setup_scopecraft"

setup() {
  TEST_DIR="$(mktemp -d)"
  setup_passing_scopecraft "$TEST_DIR"
}

teardown() {
  rm -rf "$TEST_DIR"
}

# ── Error paths ────────────────────────────────────────────────────────────────

@test "exits with code 2 when scopecraft dir missing" {
  run "$HOOK" --output-dir "$TEST_DIR/nonexistent"
  [ "$status" -eq 2 ]
}

@test "error message mentions how to generate outputs" {
  run "$HOOK" --output-dir "$TEST_DIR/nonexistent"
  [[ "$output" == *"Run a roadmap command"* ]]
}

# ── Gate 1: all_outputs_exist ──────────────────────────────────────────────────

@test "all_outputs_exist passes with 6 files" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"all_outputs_exist": { "passed": true'* ]]
}

@test "all_outputs_exist fails with 5 files" {
  rm "$TEST_DIR/scopecraft/OPEN_QUESTIONS.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"all_outputs_exist": { "passed": false'* ]]
}

# ── Gate 2: phases_in_range ────────────────────────────────────────────────────

@test "phases_in_range passes with 3 phases" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"phases_in_range": { "passed": true'* ]]
}

@test "phases_in_range fails with 2 phases" {
  printf '## Phase 1\n## Phase 2\n' > "$TEST_DIR/scopecraft/ROADMAP.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"phases_in_range": { "passed": false'* ]]
}

# ── Gate 3: stories_have_acceptance_criteria ───────────────────────────────────

@test "stories_have_acceptance_criteria passes with 5+ sections" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"stories_have_acceptance_criteria": { "passed": true'* ]]
}

@test "stories_have_acceptance_criteria fails with 4 sections" {
  printf 'Acceptance Criteria\nAcceptance Criteria\nAcceptance Criteria\nAcceptance Criteria\n' \
    > "$TEST_DIR/scopecraft/EPICS_AND_STORIES.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"stories_have_acceptance_criteria": { "passed": false'* ]]
}

# ── Gate 4: risks_documented ───────────────────────────────────────────────────

@test "risks_documented passes with 3+ risk rows" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"risks_documented": { "passed": true'* ]]
}

@test "risks_documented fails with 2 risk rows" {
  printf '| Risk | Type |\n| r1 | Technical |\n| r2 | Product |\n' \
    > "$TEST_DIR/scopecraft/RISKS_AND_DEPENDENCIES.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"risks_documented": { "passed": false'* ]]
}

# ── Gate 5: metrics_defined ────────────────────────────────────────────────────

@test "metrics_defined passes when North Star Metric present" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"metrics_defined": { "passed": true'* ]]
}

@test "metrics_defined fails when North Star Metric missing" {
  printf '# Metrics\n\nSome content.\n' > "$TEST_DIR/scopecraft/METRICS_AND_PMF.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"metrics_defined": { "passed": false'* ]]
}

# ── Gate 6: no_todo_placeholders ───────────────────────────────────────────────

@test "no_todo_placeholders passes when no placeholders" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"no_todo_placeholders": { "passed": true'* ]]
}

@test "no_todo_placeholders fails when TODO present" {
  echo "[TODO] fill this in" >> "$TEST_DIR/scopecraft/ROADMAP.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"no_todo_placeholders": { "passed": false'* ]]
}

# ── Gate 7: roadmap_has_content ────────────────────────────────────────────────

@test "roadmap_has_content passes with 50+ lines" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"roadmap_has_content": { "passed": true'* ]]
}

@test "roadmap_has_content fails with stub roadmap" {
  printf '## Phase 1\n## Phase 2\n## Phase 3\n' > "$TEST_DIR/scopecraft/ROADMAP.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"roadmap_has_content": { "passed": false'* ]]
}

# ── Gate 8: open_questions_populated ──────────────────────────────────────────

@test "open_questions_populated passes with at least one section" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"open_questions_populated": { "passed": true'* ]]
}

@test "open_questions_populated fails with no sections" {
  printf '# Open Questions\n\nNo sections here.\n' \
    > "$TEST_DIR/scopecraft/OPEN_QUESTIONS.md"
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 1 ]
  [[ "$output" == *'"open_questions_populated": { "passed": false'* ]]
}

# ── Output modes ───────────────────────────────────────────────────────────────

@test "quiet mode produces no output on pass" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --quiet
  [ "$status" -eq 0 ]
  [ -z "$output" ]
}

@test "json mode output is valid JSON structure" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"result": "PASS"'* ]]
  [[ "$output" == *'"timestamp"'* ]]
}
```

**Step 2: Install bats and run**

```bash
# On macOS:
brew install bats-core

# On Ubuntu/CI:
# sudo apt-get install -y bats

bats plugins/ralph-it-up-roadmap/tests/bash/test_validate_gates.bats
```

Expected: all tests PASS. If any fail, fix the bash validator in Task 10 first.

**Step 3: Run shellcheck one final time**

```bash
shellcheck plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh
```

**Step 4: Commit**

```bash
git add plugins/ralph-it-up-roadmap/tests/bash/
git commit -m "test: add bats tests for all 8 quality gates and output modes"
```

---

### Task 12: GitHub Actions CI workflow

**Files:**
- Create: `.github/workflows/validate.yml`

**Step 1: Write workflow**

```yaml
# .github/workflows/validate.yml
name: Validate Plugin

on:
  push:
    branches: [main]
  pull_request:

jobs:
  python-tests:
    name: Python Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r plugins/ralph-it-up-roadmap/requirements-dev.txt

      - name: Run pytest
        run: pytest plugins/ralph-it-up-roadmap/tests/python/ -v --tb=short

  bash-tests:
    name: Bash Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install bats and shellcheck
        run: sudo apt-get install -y bats shellcheck

      - name: Run shellcheck
        run: shellcheck plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh

      - name: Run bats
        run: bats plugins/ralph-it-up-roadmap/tests/bash/
```

**Step 2: Commit and push**

```bash
git add .github/workflows/validate.yml
git commit -m "ci: add GitHub Actions workflow for python and bash tests"
git push
```

**Step 3: Verify CI passes**

Open: `https://github.com/auge2u/ralph-it-up/actions`

Expected: both `Python Tests` and `Bash Tests` jobs green on first run.

If either fails, read the job log and fix before proceeding.

---

### Task 13: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update quality gates table**

In the Quality Gates section, update the gate count and add the two new gates to the table:

```markdown
| `roadmap_has_content` | `ROADMAP.md` has ≥ 50 lines |
| `open_questions_populated` | ≥ 1 `## ` section in `OPEN_QUESTIONS.md` |
```

Update the header to note there are now 8 gates (was 6).

**Step 2: Add testing section**

After the Validation section, add:

```markdown
### Running Tests Locally

```bash
# Python tests
pip install -r plugins/ralph-it-up-roadmap/requirements-dev.txt
pytest plugins/ralph-it-up-roadmap/tests/python/ -v

# Bash tests (requires bats: brew install bats-core)
bats plugins/ralph-it-up-roadmap/tests/bash/
```
```

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for 8 gates and local test commands"
git push
```

---

## Definition of Done

- [ ] `pytest plugins/ralph-it-up-roadmap/tests/python/` — all green
- [ ] `bats plugins/ralph-it-up-roadmap/tests/bash/` — all green
- [ ] `shellcheck plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh` — no warnings
- [ ] GitHub Actions CI — both jobs green on push to main
- [ ] CI blocks PRs when any gate fails (verify by checking workflow `pull_request` trigger)
- [ ] CLAUDE.md updated with 8 gates and test commands
