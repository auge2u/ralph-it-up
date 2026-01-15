---
description: Run ScopeCraft in an iterative loop until ROADMAP_COMPLETE is produced.
---

# Roadmap — ralph-it-up (ScopeCraft) Orchestrated

This command is designed for iterative orchestration: improve outputs each run until complete.

## Completion promise
When everything is complete and consistent, print the exact string:

ROADMAP_COMPLETE

## Work
Follow the ScopeCraft skill instructions and output files to `./scopecraft/`.

On each iteration, do **incremental improvement**:
- identify missing sections or weak evidence from `/docs`
- improve sequencing and dependency clarity
- tighten acceptance criteria
- refine PMF metrics and instrumentation plan
- update only what needs improvement (avoid full rewrites)

Stop only when all required outputs exist and are internally consistent, then print:
ROADMAP_COMPLETE