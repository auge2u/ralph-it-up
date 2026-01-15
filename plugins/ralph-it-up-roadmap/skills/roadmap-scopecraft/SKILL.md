---
name: roadmap-scopecraft
description: Builds a full-scope product roadmap for an existing project by scanning PRDs in /docs, extracting legacy tasks, and creating a comprehensive plan to move from MVP/early release to the next major stage.
---

You are acting as a **product owner** partnering with **senior engineers** and a **PMF-focused team**.

## When to use

Use this skill when the user asks for:
- roadmap planning from an existing repo
- converting legacy scope or pending tasks into a clean backlog
- PRD review / reconciliation across multiple documents
- maturity planning (MVP → next major stage)

## Ground rules

- Prefer evidence from the repo: `/docs`, `README`, ADRs, architecture docs, backlog/task files.
- If PRDs conflict, reconcile by:
  1) newest decision wins (when clearly dated/versioned),
  2) note divergence explicitly,
  3) propose a decision and list stakeholders needed.
- Produce outputs as files under `./scopecraft/` for easy sharing.

## Scratchpad protocol (for orchestrated mode)

When running in orchestrated/loop mode:

1. **Read first**: Check `.agent/scratchpad.md` for prior context
2. **Track progress**: Note what's done, what's remaining, blockers
3. **Update after**: Write progress to scratchpad before completing iteration

Scratchpad format:
```markdown
# Scratchpad — ralph-it-up-roadmap

## Last Updated
[timestamp]

## Progress
- [x] Completed item
- [ ] Remaining item

## Decisions Made
- [Decision and rationale]

## Blockers
- [Current blockers]

## Next Steps
- [What to do next iteration]
```

## Discovery procedure (do this first)

1) Inventory documents:
   - list PRDs and PRD-like docs in `/docs` (initial + historical)
   - identify architecture decisions (ADRs), constraints, and non-goals
2) Inventory scope sources:
   - open issues / TODOs / backlog lists / "legacy scope" notes
3) Infer current stage:
   - MVP/alpha/beta/early release signals (missing monitoring, limited permissions, minimal onboarding, weak reliability, etc.)

## Convert legacy scope into a backlog model

Normalize every task into:
- Epic
- User story (who/what/why)
- Acceptance criteria (observable, testable)
- Dependencies (tech + org)
- Risk level
- Complexity bucket (S/M/L/XL)

## Build the maturity roadmap (required structure)

Use the templates in `templates/` and produce:

### 1) VISION_AND_STAGE_DEFINITION.md
- Product vision summary (customer + problem + value)
- "Next major stage" definition with completion criteria
- Assumptions + constraints

### 2) ROADMAP.md
- 3–5 phases max
- For each phase:
  - objective (outcome)
  - key deliverables
  - definition of done
  - metrics / KPIs
  - major risks

### 3) EPICS_AND_STORIES.md
Group epics by themes:
- Core value delivery
- Adoption/onboarding
- Reliability/performance
- Security/compliance
- Developer experience / platform maturity
- Monetization/packaging (if applicable)

Each epic must include:
- user-facing intent
- stories with acceptance criteria
- dependencies and sequencing notes

### 4) RISKS_AND_DEPENDENCIES.md
- Technical risks, product risks, GTM risks
- Mitigations and contingency paths
- Dependency map (internal + external)

### 5) METRICS_AND_PMF.md
- North Star metric + supporting metrics
- PMF signals: activation funnel, retention, usage depth
- Instrumentation plan (what must be tracked to call the stage "done")

### 6) OPEN_QUESTIONS.md
- Questions blocking prioritization or delivery
- Proposed experiments or stakeholder asks to resolve them

## Completion promise

When running in orchestrated mode (ralph-orchestrator compatible):
- Iterate until outputs are complete and consistent
- Use the completion promise exactly: `LOOP_COMPLETE`
- Improve gaps rather than rewriting everything each cycle
