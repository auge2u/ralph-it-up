#!/usr/bin/env bats
# plugins/ralph-it-up-roadmap/tests/bash/test_validate_gates.bats

load "helpers/setup_scopecraft"

HOOK="$BATS_TEST_DIRNAME/../../hooks/validate-gates-handler.sh"

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

@test "json mode output contains result PASS" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"result": "PASS"'* ]]
}

@test "json mode output contains timestamp" {
  run "$HOOK" --output-dir "$TEST_DIR/scopecraft" --json
  [ "$status" -eq 0 ]
  [[ "$output" == *'"timestamp"'* ]]
}
