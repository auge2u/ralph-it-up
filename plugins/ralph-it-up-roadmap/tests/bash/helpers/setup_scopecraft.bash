#!/usr/bin/env bash
# Source this in bats tests: load "helpers/setup_scopecraft"
# Provides setup_passing_scopecraft <dir> function

HOOK="$BATS_TEST_DIRNAME/../../hooks/validate-gates-handler.sh"

setup_passing_scopecraft() {
  local dir="$1"
  mkdir -p "$dir/scopecraft"

  cat > "$dir/scopecraft/VISION_AND_STAGE_DEFINITION.md" <<'INNER'
# Vision

Content.
INNER

  # ROADMAP.md: 3 phases, >= 50 lines total
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
