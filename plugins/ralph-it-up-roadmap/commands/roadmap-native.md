---
description: Generate a roadmap using native Claude Code orchestration (no external tools required).
skill: roadmap-scopecraft
agent: roadmap-orchestrator
---

# Roadmap — Native Claude Code Orchestration

Execute the **roadmap-scopecraft** skill using the native **roadmap-orchestrator** agent. This mode requires no external dependencies like `ralph-orchestrator`.

## Features

- **Zero dependencies** — No Python packages or external tools required
- **Built-in loop control** — Iterates until quality gates pass (max 15 iterations)
- **Native validation** — Uses `hooks/validate-gates-handler.sh` for gate checks
- **Scratchpad memory** — Cross-iteration context via `.agent/scratchpad.md`

## Execution

The orchestrator will:

1. **Initialize** — Check for existing scratchpad context
2. **Execute** — Run roadmap-scopecraft skill, output to `./scopecraft/`
3. **Validate** — Check all 6 quality gates
4. **Iterate** — If gates fail, update scratchpad and repeat
5. **Complete** — Output `LOOP_COMPLETE` when all gates pass

## Quality Gates

All must pass before completion:

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 `.md` files in scopecraft/ |
| `phases_in_range` | 3-5 `## Phase` headers in ROADMAP.md |
| `stories_have_acceptance_criteria` | 5+ "Acceptance Criteria" sections |
| `risks_documented` | 3+ risk table rows |
| `metrics_defined` | "North Star Metric" section exists |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers |

## Manual Validation

You can manually run the validation hook:

```bash
# Human-readable output
./plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh

# JSON output (for scripts)
./plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh --json

# Quiet mode (exit code only)
./plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh --quiet
```

## Output Files

```
scopecraft/
├── VISION_AND_STAGE_DEFINITION.md
├── ROADMAP.md
├── EPICS_AND_STORIES.md
├── RISKS_AND_DEPENDENCIES.md
├── METRICS_AND_PMF.md
└── OPEN_QUESTIONS.md

.agent/
├── scratchpad.md           # Cross-iteration memory
└── validation-results.json # Final gate results
```

## When to Use This vs ralph-orchestrator

| Use Case | Recommended Mode |
|----------|-----------------|
| Quick roadmap generation | `/roadmap` (one-shot) |
| Iterative refinement, no setup | `/roadmap-native` (this) |
| CI/CD pipeline integration | `ralph-orchestrator` |
| Multi-backend orchestration | `ralph-orchestrator` |
| Minimal dependencies | `/roadmap-native` (this) |

## Comparison with Other Commands

| Command | Orchestration | Dependencies |
|---------|---------------|--------------|
| `/roadmap` | One-shot | None |
| `/roadmap-native` | Native loop | None |
| `/roadmap-orchestrated` | External | ralph-orchestrator |
