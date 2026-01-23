# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ralph-it-up** is a Claude Code plugin marketplace for AI-powered product roadmap generation. It transforms messy software projects (PRDs, legacy tasks, docs) into structured, product-owner scoped roadmaps for moving from MVP/early release to the next major stage.

**Current version:** 1.1.1 (see `.claude-plugin/marketplace.json`)

**ralph-orchestrator compatible** — designed to work with [ralph-orchestrator v2.2.0+](https://github.com/mikeyobrien/ralph-orchestrator) for autonomous iteration.

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry (version, plugins list)
plugins/
  ralph-it-up-roadmap/
    .claude-plugin/plugin.json     # Plugin manifest (name, version, license)
    commands/
      roadmap.md                   # One-shot slash command
      roadmap-native.md            # Native Claude Code loop (no dependencies)
      roadmap-orchestrated.md      # Loop mode (ralph-orchestrator compatible)
    agents/
      product-owner.md             # Agent persona for one-shot mode
      roadmap-orchestrator.md      # Native loop orchestrator agent
    skills/
      roadmap-scopecraft/
        SKILL.md                   # Core skill logic, quality gates, discovery procedure
        templates/                 # Output format templates (7 files)
    templates/                      # ralph-orchestrator v2 templates
      ralph.yml                    # v2 config with hat-based orchestration
      scratchpad.md                # Cross-iteration context template
      PROMPT.md                    # Optional standalone instructions
    hooks/
      validate_quality_gates.py    # Quality gate validation (Python 3, optional PyYAML)
      validate-gates-handler.sh    # Native bash validation (no dependencies)
    examples/
      scopecraft/                  # Sample outputs for reference
```

## Commands

Users invoke plugins via:
- `/ralph-it-up-roadmap:roadmap` — One-shot roadmap generation
- `/ralph-it-up-roadmap:roadmap-native` — Native Claude Code loop (no dependencies, recommended)
- `/ralph-it-up-roadmap:roadmap-orchestrated` — External orchestrator mode (ralph-orchestrator)

## Quality Gates

Quality gates are validation checks that MUST pass before `LOOP_COMPLETE`. These are defined in `validate_quality_gates.py:DEFAULT_GATES`:

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 `.md` files in scopecraft/ |
| `phases_in_range` | 3-5 `## Phase \d` headers in ROADMAP.md |
| `stories_have_acceptance_criteria` | 5+ "Acceptance Criteria" sections in EPICS_AND_STORIES.md |
| `risks_documented` | 3+ risk table rows with Technical/Product/GTM types |
| `metrics_defined` | "North Star Metric" section exists in METRICS_AND_PMF.md |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers across all outputs |

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

**Native bash validator (recommended, zero dependencies):**

```bash
# Human-readable output
./plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh

# JSON output (for scripts/CI)
./plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh --json

# Quiet mode (exit code only)
./plugins/ralph-it-up-roadmap/hooks/validate-gates-handler.sh --quiet
```

**Python validator (more features, optional PyYAML):**

```bash
# From project root (uses default gates)
python plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py

# With config file (requires: pip install pyyaml)
python plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py --config ralph.yml

# Generate markdown report (for scratchpad updates)
python plugins/ralph-it-up-roadmap/hooks/validate_quality_gates.py --markdown
```

Exit codes: `0`=pass, `1`=blocker failed, `2`=warning/not found

## Orchestration Modes

Three ways to run iterative roadmap generation:

| Mode | Command | Dependencies | Best For |
|------|---------|--------------|----------|
| **Native** (recommended) | `/roadmap-native` | None | Quick setup, minimal dependencies |
| **External** | `/roadmap-orchestrated` | `ralph-orchestrator` | CI/CD, multi-backend support |
| **One-shot** | `/roadmap` | None | Simple projects, manual iteration |

### Native Mode (New in v1.2.0)

Uses the built-in `roadmap-orchestrator` agent for autonomous looping:

```bash
/ralph-it-up-roadmap:roadmap-native
```

Features:
- Zero external dependencies
- Built-in iteration limit (15 max)
- Automatic quality gate validation
- Scratchpad memory across iterations
- JSON validation results in `.agent/validation-results.json`

### Migration from ralph-orchestrator

If you're currently using `ralph-orchestrator`, you can switch to native mode:

**Before (external orchestrator):**
```bash
pip install ralph-orchestrator
cp templates/ralph.yml ./
ralph run
```

**After (native mode):**
```bash
/ralph-it-up-roadmap:roadmap-native
```

Both modes:
- Use the same skill (`roadmap-scopecraft`)
- Produce the same outputs in `./scopecraft/`
- Follow the same quality gates
- Use `.agent/scratchpad.md` for cross-iteration memory

**When to keep using ralph-orchestrator:**
- CI/CD pipeline integration
- Multi-backend support (Gemini, Codex, etc.)
- Custom iteration limits or timeouts
- Existing ralph.yml configurations

## ralph-orchestrator Integration (v2.2.0)

For autonomous iteration with ralph-orchestrator v2:

```bash
# Install ralph-orchestrator
pip install ralph-orchestrator

# Copy templates to your project
cp plugins/ralph-it-up-roadmap/templates/ralph.yml ./ralph.yml
mkdir -p .agent
cp plugins/ralph-it-up-roadmap/templates/scratchpad.md ./.agent/scratchpad.md

# Run
ralph run

# Alternative session workflows (v2.0.8+)
ralph plan    # Structured planning mode
ralph task    # Focused task execution
```

### v2 Configuration Format

```yaml
cli:
  # Supported backends: claude, gemini, codex, qchat, aider, opencode, copilot
  backend: "claude"

event_loop:
  completion_promise: "LOOP_COMPLETE"
  max_iterations: 15
  max_runtime_seconds: 3600

hats:
  product_owner:
    triggers: ["task.start"]
    instructions: |
      # Instructions embedded here (not in separate PROMPT.md)
```

Key conventions:
- **Hat-based orchestration**: Personas defined in `hats:` section with embedded instructions
- **Completion promise**: `LOOP_COMPLETE` (only after quality gates pass)
- **Scratchpad**: `.agent/scratchpad.md` for cross-iteration context
- **Quality gates**: Now embedded in hat instructions (not separate config)
- **Validation**: `hooks/validate_quality_gates.py` still available for manual checks
- **Multi-backend**: Supports 7 backends including OpenCode (v2.0.9) and Copilot (v2.0.8)

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
Command (roadmap-native.md)         → References skill + orchestrator agent
    ↓
Agent (roadmap-orchestrator.md)     → Loop control, validation, iteration
    ↓
Skill (SKILL.md)                    → Core logic, discovery, quality gates
    ↓
Templates (templates/*.md)          → Output format specifications
    ↓
Hooks (validate-gates-handler.sh)   → Native bash validation
```

Key relationships:
- Commands declare which skill and agent to use via YAML frontmatter
- **Native mode**: `roadmap-orchestrator` agent handles loop control
- **External mode**: `ralph-orchestrator` calls Claude Code as backend
- Skills define the execution logic and reference templates for output format
- Scratchpad (`.agent/scratchpad.md`) persists state across iterations

## Contributing New Plugins

1. Create `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` manifest (name, version, author, license)
3. Add commands in `commands/` (markdown with YAML frontmatter referencing skill + agent)
4. Add skills in `skills/<skill-name>/SKILL.md`
5. Add ralph-orchestrator templates in `templates/` (ralph.yml, scratchpad.md)
6. Add validation hooks in `hooks/` (Python scripts with exit codes)
7. Register in `.claude-plugin/marketplace.json` with version and metadata

## Quality Standards

- Commands must be deterministic and file-output driven
- Skills define clear completion criteria (`LOOP_COMPLETE` for orchestrated mode)
- **Quality gates must be defined and pass before completion**
- Prefer outcomes/KRs over feature lists
- Roadmap phases limited to 3-5 max
- All outputs reference repo evidence (file paths) where possible
- Scratchpad must track progress and quality gate status between iterations
