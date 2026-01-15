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

## Scratchpad Protocol

Before each iteration, read `.agent/scratchpad.md` to understand:
- Progress from previous iterations
- Decisions made and context
- Current blockers
- Remaining work items

After each iteration, update the scratchpad with:
- What was accomplished
- What remains
- Any blockers or decisions needed

## Orchestration Rules

On each iteration, do **incremental improvement**:
- Identify missing sections or weak evidence from `/docs`
- Improve sequencing and dependency clarity
- Tighten acceptance criteria
- Refine PMF metrics and instrumentation plan
- Update only what needs improvement (avoid full rewrites)

## Completion Promise

When all outputs exist and are internally consistent, print exactly:

```
LOOP_COMPLETE
```

This marker signals ralph-orchestrator to stop iteration.
