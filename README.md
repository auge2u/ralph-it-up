# ralph-it-up

**ralph-it-up** is a public marketplace of AI skills for turning real, messy software projects into
**clear, product-owner scoped roadmaps** — from **MVP/early release → next major stage**.

It is designed to work **one-shot** or in an **orchestrated loop** (iterate until “done”).

## What’s included

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

One-shot:

```txt
/ralph-it-up-roadmap:roadmap
```

Orchestrated (loop-friendly):

```txt
/ralph-it-up-roadmap:roadmap-orchestrated
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

## License

MIT
