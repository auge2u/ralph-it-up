# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ralph-it-up** is a Claude Code plugin marketplace for AI-powered product roadmap generation. It transforms messy software projects (PRDs, legacy tasks, docs) into structured, product-owner scoped roadmaps for moving from MVP/early release to the next major stage.

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry (lists available plugins)
plugins/
  ralph-it-up-roadmap/
    .claude-plugin/plugin.json     # Plugin manifest
    commands/                       # User-invocable slash commands
      roadmap.md                   # One-shot roadmap generation
      roadmap-orchestrated.md      # Iterative loop mode
    agents/
      product-owner.md             # Agent persona definition
    skills/
      roadmap-scopecraft/
        SKILL.md                   # Core skill logic
        templates/                 # Output format templates
```

## Commands

Users invoke plugins via:
- `/ralph-it-up-roadmap:roadmap` — One-shot roadmap generation
- `/ralph-it-up-roadmap:roadmap-orchestrated` — Iterative mode (loops until `ROADMAP_COMPLETE`)

## How the Skill Works

1. **Discovery**: Scans `/docs` for PRDs, README, CHANGELOG, ADRs, architecture docs, open TODOs, and backlog files
2. **Reconciliation**: Resolves conflicts between PRDs (newest wins, or explicit divergence noted)
3. **Normalization**: Converts legacy scope into Epic → Story → Acceptance Criteria structure
4. **Output**: Writes 6 files to `./scopecraft/`:
   - `VISION_AND_STAGE_DEFINITION.md`
   - `ROADMAP.md` (3-5 phases max)
   - `EPICS_AND_STORIES.md`
   - `RISKS_AND_DEPENDENCIES.md`
   - `METRICS_AND_PMF.md`
   - `OPEN_QUESTIONS.md`

## Contributing New Plugins

1. Create `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` manifest
3. Add commands in `commands/` (markdown with frontmatter)
4. Add skills in `skills/` with `SKILL.md`
5. Register in `.claude-plugin/marketplace.json`

## Quality Standards

- Commands must be deterministic and file-output driven
- Skills define clear completion criteria
- Prefer outcomes/KRs over feature lists
- Roadmap phases limited to 3-5 max
- All outputs reference repo evidence (file paths) where possible
