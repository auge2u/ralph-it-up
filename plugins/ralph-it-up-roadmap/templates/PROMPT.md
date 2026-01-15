# Task: Generate Product Roadmap

You are a **product owner** generating a comprehensive roadmap for this repository.

## Objective

Scan the codebase and documentation to produce a complete maturity roadmap that moves the project from its current stage (MVP/early release) to the next major stage.

## Instructions

1. **Discovery Phase**
   - Scan `/docs` for PRDs (initial + historical)
   - Review `README`, `CHANGELOG`, ADRs, architecture docs
   - Inventory open TODOs, issues, backlog files
   - Identify current maturity stage

2. **Output Phase**
   Create the following files under `./scopecraft/`:
   - `VISION_AND_STAGE_DEFINITION.md`
   - `ROADMAP.md` (3-5 phases max)
   - `EPICS_AND_STORIES.md`
   - `RISKS_AND_DEPENDENCIES.md`
   - `METRICS_AND_PMF.md`
   - `OPEN_QUESTIONS.md`

3. **Scratchpad Protocol**
   - Read `.agent/scratchpad.md` at start of each iteration
   - Update scratchpad with progress after each iteration
   - Track: completed items, remaining work, blockers, decisions

4. **Quality Standards**
   - Be explicit, practical, senior-engineer-friendly
   - Optimize for PMF and delivery feasibility
   - Include acceptance criteria for all stories
   - Reference repo evidence (file paths) where possible

## Completion

When all outputs exist and are internally consistent, print:

```
LOOP_COMPLETE
```

<!--
Run with ralph-orchestrator:
  ralph run -a claude --max-iterations 10
-->
