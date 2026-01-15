# Roadmap

> Example output from ralph-it-up-roadmap plugin

## Phase 1 — Foundation

**Objective (Outcome):** Establish a working plugin marketplace with one high-quality plugin
**Customer Value:** Users can generate roadmaps from existing repos
**Deliverables:**
- Marketplace manifest structure
- ralph-it-up-roadmap plugin
- Installation documentation

**Dependencies:** Claude Code plugin system
**Risks + Mitigations:**
- Plugin API changes → Pin to stable version, monitor changelog

**Metrics / KRs:**
- 1 plugin published
- Installation instructions tested on 3 machines

**Definition of Done:** Plugin installs and runs successfully on fresh Claude Code setup

---

## Phase 2 — Quality & Templates

**Objective (Outcome):** Improve output consistency and reduce manual formatting
**Customer Value:** Reliable, professional-looking roadmap artifacts
**Deliverables:**
- Complete template set for all 6 output files
- Example outputs for reference
- Validation tooling

**Dependencies:** Phase 1 complete
**Risks + Mitigations:**
- Template bloat → Keep templates minimal, focus on structure not content

**Metrics / KRs:**
- 100% template coverage
- Output passes linting

**Definition of Done:** All outputs match templates, examples documented

---

## Phase 3 — Ecosystem Growth

**Objective (Outcome):** Attract community contributions and expand plugin variety
**Customer Value:** More specialized roadmap workflows available
**Deliverables:**
- Plugin contribution guide
- Plugin validation CI
- 2+ community plugins

**Dependencies:** Phase 2 complete
**Risks + Mitigations:**
- Low adoption → Promote in Claude Code community, write blog post

**Metrics / KRs:**
- 3+ total plugins
- 1+ external contributor

**Definition of Done:** External contributor successfully publishes plugin
