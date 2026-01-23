# Hooks

Validation hooks for ralph-it-up-roadmap quality gates.

## validate-gates-handler.sh (Recommended)

Native bash script for quality gate validation. Zero dependencies, works everywhere.

### Usage

```bash
# Human-readable output (default)
./validate-gates-handler.sh

# JSON output (for scripts/CI)
./validate-gates-handler.sh --json

# Quiet mode (exit code only)
./validate-gates-handler.sh --quiet

# Custom output directory
./validate-gates-handler.sh --output-dir ./my-scopecraft
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All gates passed |
| 1 | Blocker gates failed |
| 2 | scopecraft directory not found |

### Example JSON Output

```json
{
  "timestamp": "2026-01-23T10:30:00Z",
  "gates": {
    "all_outputs_exist": { "passed": true, "details": "6 files" },
    "phases_in_range": { "passed": true, "details": "4 phases" },
    "stories_have_acceptance_criteria": { "passed": true, "details": "8 sections" },
    "risks_documented": { "passed": true, "details": "5 risks" },
    "metrics_defined": { "passed": true, "details": "Section found" },
    "no_todo_placeholders": { "passed": true, "details": "0 placeholders" }
  },
  "result": "PASS"
}
```

---

## validate_quality_gates.py

Python script to validate scopecraft outputs against quality gate definitions.

### Installation

```bash
# Optional: install PyYAML for config file support
pip install pyyaml
```

### Usage

```bash
# Run with default gates
python validate_quality_gates.py

# Run with custom config
python validate_quality_gates.py --config ralph.yml

# Run against specific output directory
python validate_quality_gates.py --output-dir ./scopecraft

# Verbose output
python validate_quality_gates.py --verbose

# Output markdown report
python validate_quality_gates.py --markdown

# Append results to scratchpad
python validate_quality_gates.py --scratchpad .agent/scratchpad.md
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All gates passed |
| 1 | Blocker gates failed |
| 2 | Warning gates failed (no blockers) |

### Integration with ralph-orchestrator

**v2.0.0 (current):** Quality gates are embedded in hat instructions. Use this script for:
- Manual validation before committing
- CI pipeline checks
- Debugging gate failures

```bash
# Validate outputs after ralph completes
python validate_quality_gates.py --output-dir ./scopecraft --markdown
```

**v1.x (legacy):** Could be added as a post-iteration hook in ralph.yml.

### Quality Gate Types

| Check Type | Description | Parameters |
|------------|-------------|------------|
| `file_count` | Count files matching glob | `path`, `expect` |
| `min_lines` | Minimum line count | `path`, `min` |
| `pattern_count` | Count regex matches | `path`, `pattern`, `min`, `max` |
| `pattern_exists` | Verify pattern exists | `path`, `pattern` |

### Example Output

```
============================================================
QUALITY GATE VALIDATION RESULTS
============================================================

✓ PASS [all_outputs_exist] All required outputs exist
       Found 6 files

✓ PASS [phases_in_range] Roadmap has 3-5 phases
       Found 4 matches

✗ FAIL [no_todo_placeholders] No TODO placeholders remain
       Expected <= 0, found 2

------------------------------------------------------------
Total: 7 | Passed: 6 | Blockers: 1 | Warnings: 0
------------------------------------------------------------

❌ QUALITY GATES FAILED - Cannot issue LOOP_COMPLETE
```
