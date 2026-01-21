# Task: Generate Product Roadmap

> **Note:** In ralph-orchestrator v2.0.0, instructions are embedded in `ralph.yml` under the `hats.product_owner.instructions` field. This file is provided for standalone use or customization.

You are a **product owner** generating a comprehensive roadmap for this repository.

## Objective

Scan the codebase and documentation to produce a complete maturity roadmap that moves the project from its current stage (MVP/early release) to the next major stage.

## Instructions

1. **Scratchpad Protocol**
   - Read `.agent/scratchpad.md` at start of each iteration
   - Update scratchpad with progress after each iteration
   - Track: completed items, remaining work, blockers, decisions

2. **Discovery Phase**
   - Scan `/docs` for PRDs (initial + historical)
   - Review `README`, `CHANGELOG`, ADRs, architecture docs
   - Inventory open TODOs, issues, backlog files
   - Identify current maturity stage

3. **Output Phase**
   Create the following files under `./scopecraft/`:
   - `VISION_AND_STAGE_DEFINITION.md`
   - `ROADMAP.md` (3-5 phases max)
   - `EPICS_AND_STORIES.md`
   - `RISKS_AND_DEPENDENCIES.md`
   - `METRICS_AND_PMF.md`
   - `OPEN_QUESTIONS.md`

4. **Quality Standards**
   - Be explicit, practical, senior-engineer-friendly
   - Optimize for PMF and delivery feasibility
   - Include acceptance criteria for all stories
   - Reference repo evidence (file paths) where possible

## Quality Gates (MUST PASS)

Before completing, validate ALL of these conditions:

| Gate | Requirement |
|------|-------------|
| all_outputs_exist | 6 files in scopecraft/ |
| phases_in_range | 3-5 `## Phase` headers in ROADMAP.md |
| epics_have_stories | 5+ `#### Story` headers |
| stories_have_acceptance_criteria | 5+ "Acceptance Criteria" sections |
| risks_documented | 3+ risk table rows with Technical/Product/GTM |
| metrics_defined | "North Star Metric" section exists |
| no_todo_placeholders | Zero `[TODO]`, `[TBD]`, `[PLACEHOLDER]` markers |

## Completion

When all outputs exist, are internally consistent, and ALL quality gates pass:

```
LOOP_COMPLETE
```

**DO NOT issue LOOP_COMPLETE if any quality gate fails.**
