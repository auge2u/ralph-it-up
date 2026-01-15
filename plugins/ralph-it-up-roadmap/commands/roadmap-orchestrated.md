---
description: Run ScopeCraft in an iterative loop until LOOP_COMPLETE. Compatible with ralph-orchestrator.
skill: roadmap-scopecraft
agent: product-owner
---

# Roadmap — ralph-it-up (ScopeCraft) Orchestrated

Execute the **roadmap-scopecraft** skill in iterative mode, compatible with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator).

## Execution

1. Follow all instructions in `skills/roadmap-scopecraft/SKILL.md`
2. Use templates from `skills/roadmap-scopecraft/templates/`
3. Output all files to `./scopecraft/`
4. Track progress in `.agent/scratchpad.md`
5. **Validate quality gates before completing**

## Scratchpad Protocol

Before each iteration, read `.agent/scratchpad.md` to understand:
- Progress from previous iterations
- Quality gate status from last check
- Decisions made and context
- Current blockers
- Remaining work items

After each iteration, update the scratchpad with:
- What was accomplished
- Quality gate validation results
- What remains
- Any blockers or decisions needed

## Quality Gates (MUST PASS)

Before issuing `LOOP_COMPLETE`, validate ALL blocker gates:

| Gate | Check | Requirement |
|------|-------|-------------|
| all_outputs_exist | File count | 6 files in scopecraft/ |
| phases_in_range | Pattern count | 3-5 `## Phase` headers |
| epics_have_stories | Pattern count | 5+ `#### Story` headers |
| stories_have_acceptance_criteria | Pattern count | 5+ "Acceptance Criteria" |
| risks_documented | Pattern count | 3+ risk table rows |
| metrics_defined | Pattern exists | "North Star Metric" section |
| no_todo_placeholders | Pattern count | 0 `[TODO]`/`[TBD]`/`[PLACEHOLDER]` |

### Self-Validation Checklist

Run through this checklist before each completion attempt:

```
□ scopecraft/ has exactly 6 .md files
□ ROADMAP.md has 3-5 "## Phase N" sections
□ EPICS_AND_STORIES.md has 5+ "#### Story" sections
□ Each story has "Acceptance Criteria:" section
□ RISKS_AND_DEPENDENCIES.md has 3+ table rows with risk types
□ METRICS_AND_PMF.md has "North Star Metric" section
□ No [TODO], [TBD], or [PLACEHOLDER] markers anywhere
```

If ANY check fails → continue iterating, update scratchpad with failures.

## Orchestration Rules

On each iteration, do **incremental improvement**:
- Identify missing sections or weak evidence from `/docs`
- Improve sequencing and dependency clarity
- Tighten acceptance criteria
- Refine PMF metrics and instrumentation plan
- **Fix any failing quality gates**
- Update only what needs improvement (avoid full rewrites)

## Completion Promise

When ALL quality gates pass and outputs are internally consistent, print exactly:

```
LOOP_COMPLETE
```

This marker signals ralph-orchestrator to stop iteration.

**⚠️ DO NOT issue LOOP_COMPLETE if any blocker gate fails.**
