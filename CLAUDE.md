# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ralph-it-up** is a Claude Code plugin marketplace for AI-powered product roadmap generation. It transforms messy software projects (PRDs, legacy tasks, docs) into structured, product-owner scoped roadmaps for moving from MVP/early release to the next major stage.

**ralph-orchestrator compatible** — designed to work with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) for autonomous iteration.

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry (lists available plugins)
plugins/
  ralph-it-up-roadmap/
    .claude-plugin/plugin.json     # Plugin manifest
    commands/                       # User-invocable slash commands
      roadmap.md                   # One-shot roadmap generation
      roadmap-orchestrated.md      # Iterative loop mode (ralph-orchestrator compatible)
    agents/
      product-owner.md             # Agent persona definition
    skills/
      roadmap-scopecraft/
        SKILL.md                   # Core skill logic with quality gates
        templates/                 # Output format templates
    templates/                      # ralph-orchestrator templates
      PROMPT.md                    # Task definition for ralph run
      ralph.yml                    # Orchestrator config with quality gates
      scratchpad.md                # Cross-iteration context template
    hooks/
      validate_quality_gates.py    # Quality gate validation script
    examples/
      scopecraft/                  # Sample outputs
```

## Commands

Users invoke plugins via:
- `/ralph-it-up-roadmap:roadmap` — One-shot roadmap generation
- `/ralph-it-up-roadmap:roadmap-orchestrated` — Iterative mode (loops until `LOOP_COMPLETE`)

## Quality Gates

Quality gates are validation checks that MUST pass before `LOOP_COMPLETE`:

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 files in scopecraft/ |
| `phases_in_range` | 3-5 `## Phase` headers in ROADMAP.md |
| `epics_have_stories` | 5+ `#### Story` headers |
| `stories_have_acceptance_criteria` | 5+ "Acceptance Criteria" sections |
| `risks_documented` | 3+ risk table rows |
| `metrics_defined` | "North Star Metric" section exists |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]` markers |

### Required Output Files (6 total)

```
scopecraft/
├── VISION_AND_STAGE_DEFINITION.md
├── ROADMAP.md
├── EPICS_AND_STORIES.md
├── RISKS_AND_DEPENDENCIES.md
├── METRICS_AND_PMF.md
└── OPEN_QUESTIONS.md
```

### Validation

```bash
# From project root (uses default gates)
python plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py

# With config file (requires PyYAML)
python plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py --config ralph.yml

# Generate markdown report
python plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py --markdown

# Exit codes: 0=pass, 1=blocker failed, 2=warning only
```

## ralph-orchestrator Integration

For autonomous iteration with ralph-orchestrator:

```bash
ralph run -a claude
```

Key conventions:
- **Completion promise**: `LOOP_COMPLETE` (only after quality gates pass)
- **Scratchpad**: `.agent/scratchpad.md` for cross-iteration context
- **Config**: `ralph.yml` with iteration/cost limits and quality gates
- **Validation**: `hooks/validate_quality_gates.py`

## How the Skill Works

1. **Discovery**: Scans `/docs` for PRDs, README, CHANGELOG, ADRs, architecture docs, open TODOs, and backlog files
2. **Scratchpad**: Reads `.agent/scratchpad.md` for prior context (orchestrated mode)
3. **Reconciliation**: Resolves conflicts between PRDs (newest wins, or explicit divergence noted)
4. **Normalization**: Converts legacy scope into Epic → Story → Acceptance Criteria structure
5. **Output**: Writes 6 files to `./scopecraft/`
6. **Validation**: Checks quality gates before completion
7. **Update scratchpad**: Records progress and gate status for next iteration

## Plugin Architecture

```
Command (roadmap.md)           → References skill + agent
    ↓
Agent (product-owner.md)       → Defines persona for execution
    ↓
Skill (SKILL.md)               → Core logic, discovery, quality gates
    ↓
Templates (templates/*.md)     → Output format specifications
    ↓
Hooks (validate_quality_gates.py) → Automated validation
```

Key relationships:
- Commands declare which skill and agent to use via YAML frontmatter
- Skills define the execution logic and reference templates for output format
- `ralph.yml` overrides default quality gates when present
- Scratchpad (`.agent/scratchpad.md`) persists state across orchestrator iterations

## Contributing New Plugins

1. Create `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` manifest
3. Add commands in `commands/` (markdown with frontmatter)
4. Add skills in `skills/` with `SKILL.md`
5. Add ralph-orchestrator templates in `templates/` (PROMPT.md, ralph.yml, scratchpad.md)
6. Add validation hooks in `hooks/`
7. Register in `.claude-plugin/marketplace.json`

## Quality Standards

- Commands must be deterministic and file-output driven
- Skills define clear completion criteria (`LOOP_COMPLETE` for orchestrated mode)
- **Quality gates must be defined and pass before completion**
- Prefer outcomes/KRs over feature lists
- Roadmap phases limited to 3-5 max
- All outputs reference repo evidence (file paths) where possible
- Scratchpad must track progress and quality gate status between iterations
