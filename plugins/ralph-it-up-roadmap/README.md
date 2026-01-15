# ralph-it-up-roadmap

Generate a full-scope product roadmap from an existing repository by scanning docs/PRDs and legacy tasks.

**ralph-orchestrator compatible** — works standalone or with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) for autonomous iteration.

## Commands

### Roadmap (one-shot)
```txt
/ralph-it-up-roadmap:roadmap
```

### Roadmap (orchestrated loop)
```txt
/ralph-it-up-roadmap:roadmap-orchestrated
```

## What it produces

Creates a `./scopecraft/` directory containing:
- Vision + definition of "next major stage"
- Roadmap phases with outcomes/KRs
- Epics & stories with acceptance criteria
- Risk register + dependencies
- PMF metrics + instrumentation outline
- Open questions / decisions needed

## Examples

See `examples/scopecraft/` for sample outputs demonstrating expected format and detail level.

## Quality Gates

Quality gates are validation checks that **MUST pass** before `LOOP_COMPLETE` can be issued.

### Default Gates

| Gate | Type | Requirement |
|------|------|-------------|
| `all_outputs_exist` | file_count | 6 files in scopecraft/ |
| `phases_in_range` | pattern_count | 3-5 `## Phase` headers |
| `epics_have_stories` | pattern_count | 5+ `#### Story` headers |
| `stories_have_acceptance_criteria` | pattern_count | 5+ "Acceptance Criteria" |
| `risks_documented` | pattern_count | 3+ risk table rows |
| `metrics_defined` | pattern_exists | "North Star Metric" section |
| `no_todo_placeholders` | pattern_count | 0 `[TODO]`/`[TBD]` markers |

### Running Validation

```bash
# Validate outputs manually
python hooks/validate_quality_gates.py

# With verbose output
python hooks/validate_quality_gates.py --verbose

# Append to scratchpad
python hooks/validate_quality_gates.py --scratchpad .agent/scratchpad.md
```

### Customizing Gates

Edit `ralph.yml` to adjust thresholds or add custom gates:

```yaml
quality_gates:
  - id: my_custom_gate
    name: "Custom validation"
    check: "pattern_count"
    path: "scopecraft/*.md"
    pattern: "my-pattern"
    min: 1
    severity: blocker
```

## ralph-orchestrator Integration

For autonomous iteration with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator):

### Quick Start

```bash
# Install ralph-orchestrator
pip install ralph-orchestrator

# Copy templates to your project
cp templates/PROMPT.md ./PROMPT.md
cp templates/ralph.yml ./ralph.yml
mkdir -p .agent && cp templates/scratchpad.md ./.agent/scratchpad.md

# Run orchestrated roadmap generation
ralph run -a claude
```

### Configuration

Edit `ralph.yml` to adjust:
- `max_iterations` — default 15, increase for complex projects
- `max_runtime` — default 1 hour
- `max_cost` — default $25 USD ceiling
- `checkpoint_interval` — git commits every N iterations
- `quality_gates` — validation rules for outputs

### Completion Promise

The skill uses `LOOP_COMPLETE` as its completion marker, compatible with ralph-orchestrator defaults.

**Quality gates MUST pass before LOOP_COMPLETE is issued.**

### Scratchpad

Progress is tracked in `.agent/scratchpad.md` between iterations, enabling:
- Incremental improvement (not full rewrites)
- Quality gate status tracking
- Recovery from interruptions
- Visibility into agent progress
