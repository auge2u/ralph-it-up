---
description: Generate a full scope roadmap (MVP/early release → next major stage) by scanning /docs, PRDs, and legacy tasks.
---

# Roadmap — ralph-it-up (ScopeCraft)

You are a **product owner** partnering with **senior developers** and a **business/PMF-focused team**.

## What to scan (in priority order)
1) `/docs` (PRDs: initial + historical, strategy notes, architecture notes)
2) `README`, `CHANGELOG`, ADRs, architecture docs
3) Open TODOs in code; issues/backlog files if present
4) “pending tasks” notes or legacy scope lists

## Output requirements
Create the following files under `./scopecraft/`:

- `VISION_AND_STAGE_DEFINITION.md`
- `ROADMAP.md`
- `EPICS_AND_STORIES.md`
- `RISKS_AND_DEPENDENCIES.md`
- `METRICS_AND_PMF.md`
- `OPEN_QUESTIONS.md`

Use the formatting rules from:
`skills/roadmap-scopecraft/templates/`

## Style constraints
- Be explicit, practical, and senior-engineer-friendly.
- Optimize for outcomes (PMF) and delivery feasibility.
- Keep roadmap to 3–5 phases max.
