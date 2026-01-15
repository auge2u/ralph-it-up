# Metrics and PMF

> Example output from ralph-it-up-roadmap plugin

## North Star Metric

**Metric:** Roadmaps generated per week
**Target:** 50 roadmaps/week by end of Phase 3
**Why:** Directly measures value delivery to users

## Supporting Metrics

| Metric | Current | Target | Rationale |
|--------|---------|--------|-----------|
| Plugin installs | 0 | 100 | Adoption indicator |
| Completion rate | N/A | 80% | Users finish roadmap generation |
| Return usage (7-day) | N/A | 30% | Ongoing value, not one-time |
| Template adherence | N/A | 95% | Output quality consistency |

## PMF Signals

### Activation Funnel

1. **Discover plugin** → 100%
2. **Install plugin** → 60% target
3. **Run first roadmap** → 80% of installs
4. **Complete roadmap** → 80% of runs
5. **Use output artifacts** → 70% of completions

### Retention

- **D1:** 50% (run again next day)
- **D7:** 30% (weekly roadmap refresh)
- **D30:** 20% (monthly planning cycle)

### Usage Depth

- Average phases per roadmap: 3-5
- Average stories per epic: 3-5
- Open questions resolved: >80%

## Instrumentation Plan

| Event | Trigger | Properties | Priority |
|-------|---------|------------|----------|
| `plugin_installed` | Install completes | plugin_name, version | P0 |
| `roadmap_started` | Command invoked | mode (oneshot/orchestrated) | P0 |
| `roadmap_completed` | ROADMAP_COMPLETE printed | duration_seconds, file_count | P0 |
| `template_used` | Template file read | template_name | P1 |
| `error_occurred` | Exception thrown | error_type, context | P0 |
