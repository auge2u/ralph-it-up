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

**Dependencies:**
- Python 3.8+
- pytest installed

---

## Phase 2 — Growth

**Objective:** Expand coverage and improve reliability.

**Customer Value:** Users trust outputs are complete.

**Deliverables:**
- Extended quality gates
- CI integration

**Metrics / KRs:**
- CI runs in under 60 seconds

**Dependencies:**
- GitHub Actions configured
- Branch protection enabled

---

## Phase 3 — Scale

**Objective:** Support community contributions.

**Customer Value:** External contributors can add plugins.

**Deliverables:**
- Plugin contribution guide
- Automated submission validation

**Metrics / KRs:**
- 3+ plugins in marketplace

**Dependencies:**
- Contributor documentation published
- Marketplace registry automated

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
