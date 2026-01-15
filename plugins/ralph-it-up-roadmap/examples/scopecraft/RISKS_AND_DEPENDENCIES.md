# Risks and Dependencies

> Example output from ralph-it-up-roadmap plugin

## Risk Register

| Risk | Type | Likelihood | Impact | Mitigation | Owner | Trigger/Signal |
|------|------|------------|--------|------------|-------|----------------|
| Claude Code plugin API changes | Technical | Medium | High | Pin versions, monitor changelog, abstract plugin interface | Tech Lead | Breaking change in release notes |
| Low community adoption | Product | Medium | Medium | Active promotion, quality examples, responsive support | Product | <10 installs after 30 days |
| Output quality inconsistency | Product | Low | Medium | Comprehensive templates, validation checks | Tech Lead | User complaints about formatting |
| Scope creep in roadmap features | Product | High | Medium | Strict phase gates, say no to nice-to-haves | Product | Phase exceeds 5 deliverables |

## Technical Dependencies

| Dependency | Type | Status | Risk Level | Fallback |
|------------|------|--------|------------|----------|
| Claude Code CLI | External | Stable | Low | None (hard requirement) |
| Markdown rendering | External | Stable | Low | Plain text fallback |
| Git for version control | External | Stable | Low | Manual file management |

## Organizational Dependencies

| Dependency | Owner | Status | Needed By |
|------------|-------|--------|-----------|
| Plugin marketplace approval | Claude Code team | Pending | Phase 1 |
| Community guidelines review | Legal | Not started | Phase 3 |

## Dependency Map

```
Phase 1: Foundation
    └── Claude Code plugin system (external)

Phase 2: Quality
    └── Phase 1 complete (internal)

Phase 3: Ecosystem
    ├── Phase 2 complete (internal)
    └── Community guidelines (organizational)
```
