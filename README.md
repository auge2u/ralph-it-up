# ralph-it-up

**ralph-it-up** is a public marketplace of AI skills for turning real, messy software projects into
**clear, product-owner scoped roadmaps** — from **MVP/early release → next major stage**.

It is designed to work **one-shot** or in an **orchestrated loop** with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator).

## What's included

### Plugin: `ralph-it-up-roadmap`
A skill-driven workflow that:
- scans `/docs` for PRDs (including older/legacy PRDs),
- inventories pending/legacy tasks (wherever they live),
- reconciles conflicting requirements,
- outputs a maturity roadmap, epics/stories, risks, and metrics.

## Install (Claude Code)

```txt
/plugin marketplace add auge2u/ralph-it-up
/plugin install ralph-it-up-roadmap@ralph-it-up
```

## Run

### One-shot (Claude Code)

```txt
/ralph-it-up-roadmap:roadmap
```

### Orchestrated loop (Claude Code)

```txt
/ralph-it-up-roadmap:roadmap-orchestrated
```

### With ralph-orchestrator (v2.0.0)

For fully autonomous iteration with [ralph-orchestrator v2](https://github.com/mikeyobrien/ralph-orchestrator):

```bash
# Install ralph-orchestrator
pip install ralph-orchestrator

# Copy templates to your project
cp plugins/ralph-it-up-roadmap/templates/ralph.yml ./ralph.yml
mkdir -p .agent
cp plugins/ralph-it-up-roadmap/templates/scratchpad.md ./.agent/scratchpad.md

# Run (v2 uses hat-based config, no -a flag needed)
ralph run
```

> **Note:** v2 uses hat-based orchestration with instructions embedded in `ralph.yml`. The separate `PROMPT.md` is optional and provided for standalone use.

## Outputs

The skill writes files to:
- `./scopecraft/`

Including:
- `VISION_AND_STAGE_DEFINITION.md`
- `ROADMAP.md`
- `EPICS_AND_STORIES.md`
- `RISKS_AND_DEPENDENCIES.md`
- `METRICS_AND_PMF.md`
- `OPEN_QUESTIONS.md`

## ralph-orchestrator Compatibility (v2.0.0)

This plugin is fully compatible with [ralph-orchestrator v2](https://github.com/mikeyobrien/ralph-orchestrator):

| Feature | Support |
|---------|---------|
| Completion promise | `LOOP_COMPLETE` |
| Scratchpad | `.agent/scratchpad.md` |
| Hat-based orchestration | `product_owner` hat with embedded instructions |
| ralph.yml | v2 config template included |
| Multi-backend | claude (default), gemini, codex, etc. |
| Quality gates | Embedded in hat instructions |

## License

MIT
