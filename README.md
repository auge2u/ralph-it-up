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

### With ralph-orchestrator

For fully autonomous iteration:

```bash
# Install ralph-orchestrator
pip install ralph-orchestrator

# Copy templates to your project
cp plugins/ralph-it-up-roadmap/templates/PROMPT.md ./PROMPT.md
cp plugins/ralph-it-up-roadmap/templates/ralph.yml ./ralph.yml
mkdir -p .agent
cp plugins/ralph-it-up-roadmap/templates/scratchpad.md ./.agent/scratchpad.md

# Run
ralph run -a claude
```

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

## ralph-orchestrator Compatibility

This plugin is fully compatible with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator):

| Feature | Support |
|---------|---------|
| Completion promise | `LOOP_COMPLETE` |
| Scratchpad | `.agent/scratchpad.md` |
| PROMPT.md | Template included |
| ralph.yml | Config template included |
| Git checkpointing | Supported |

## License

MIT
