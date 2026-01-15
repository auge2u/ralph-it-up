# Hooks

Validation hooks for ralph-it-up-roadmap quality gates.

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

Add to your workflow as a post-iteration hook:

```yaml
# ralph.yml
hooks:
  post_iteration:
    - python hooks/validate_quality_gates.py --scratchpad .agent/scratchpad.md
```

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
