#!/usr/bin/env bash
# Source this in bats tests: load "helpers/setup_scopecraft"
# Provides setup_passing_scopecraft <dir> function

setup_passing_scopecraft() {
  local dir="$1"
  mkdir -p "$dir/scopecraft" || return 1

  cat > "$dir/scopecraft/VISION_AND_STAGE_DEFINITION.md" <<'INNER'
# Vision

Content.
INNER

  cat > "$dir/scopecraft/ROADMAP.md" <<'INNER'
# Roadmap

## Phase 1 — Foundation

**Objective:** Establish core infrastructure.

**Customer Value:** Users can run the plugin end-to-end.

**Deliverables:**
- Core validation logic
- Basic test coverage
- CI integration
- Documentation

**Metrics / KRs:**
- All gates pass on first run
- CI under 60 seconds

---

## Phase 2 — Growth

**Objective:** Expand coverage and reliability.

**Customer Value:** Users trust outputs are complete.

**Deliverables:**
- Extended quality gates
- Error handling improvements
- Contributor documentation
- Template gallery

**Metrics / KRs:**
- CI runs in under 60 seconds
- Zero manual validation steps

---

## Phase 3 — Scale

**Objective:** Support community contributions.

**Customer Value:** External contributors can add plugins.

**Deliverables:**
- Plugin contribution guide
- Automated submission validation
- Community recognition
- Catalog page

**Metrics / KRs:**
- 3+ plugins in marketplace
- External contributor merged

---
INNER

  cat > "$dir/scopecraft/EPICS_AND_STORIES.md" <<'INNER'
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
INNER

  cat > "$dir/scopecraft/RISKS_AND_DEPENDENCIES.md" <<'INNER'
| Risk | Type | Notes |
|------|------|-------|
| Risk 1 | Technical | note |
| Risk 2 | Product | note |
| Risk 3 | GTM | note |
INNER

  cat > "$dir/scopecraft/METRICS_AND_PMF.md" <<'INNER'
# Metrics

## North Star Metric

Time-to-first-roadmap.
INNER

  cat > "$dir/scopecraft/OPEN_QUESTIONS.md" <<'INNER'
# Open Questions

## Question 1

Details here.
INNER
}
