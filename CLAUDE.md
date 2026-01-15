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
        SKILL.md                   # Core skill logic with scratchpad protocol
        templates/                 # Output format templates
    templates/                      # ralph-orchestrator templates
      PROMPT.md                    # Task definition for ralph run
      ralph.yml                    # Orchestrator configuration
      scratchpad.md                # Cross-iteration context template
    examples/
      scopecraft/                  # Sample outputs
```

## Commands

Users invoke plugins via:
- `/ralph-it-up-roadmap:roadmap` — One-shot roadmap generation
- `/ralph-it-up-roadmap:roadmap-orchestrated` — Iterative mode (loops until `LOOP_COMPLETE`)

## ralph-orchestrator Integration

For autonomous iteration with ralph-orchestrator:

```bash
ralph run -a claude
```

Key conventions:
- **Completion promise**: `LOOP_COMPLETE` (not ROADMAP_COMPLETE)
- **Scratchpad**: `.agent/scratchpad.md` for cross-iteration context
- **Config**: `ralph.yml` with iteration/cost limits

## How the Skill Works

1. **Discovery**: Scans `/docs` for PRDs, README, CHANGELOG, ADRs, architecture docs, open TODOs, and backlog files
2. **Scratchpad**: Reads `.agent/scratchpad.md` for prior context (orchestrated mode)
3. **Reconciliation**: Resolves conflicts between PRDs (newest wins, or explicit divergence noted)
4. **Normalization**: Converts legacy scope into Epic → Story → Acceptance Criteria structure
5. **Output**: Writes 6 files to `./scopecraft/`
6. **Update scratchpad**: Records progress for next iteration (orchestrated mode)

## Contributing New Plugins

1. Create `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` manifest
3. Add commands in `commands/` (markdown with frontmatter)
4. Add skills in `skills/` with `SKILL.md`
5. Add ralph-orchestrator templates in `templates/` (PROMPT.md, ralph.yml, scratchpad.md)
6. Register in `.claude-plugin/marketplace.json`

## Quality Standards

- Commands must be deterministic and file-output driven
- Skills define clear completion criteria (`LOOP_COMPLETE` for orchestrated mode)
- Prefer outcomes/KRs over feature lists
- Roadmap phases limited to 3-5 max
- All outputs reference repo evidence (file paths) where possible
- Scratchpad must track progress between iterations
