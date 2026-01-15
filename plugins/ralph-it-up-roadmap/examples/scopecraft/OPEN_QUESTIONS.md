# Open Questions

> Example output from ralph-it-up-roadmap plugin

## Blocking Questions

### Q1: Plugin distribution model

**Context:** Currently plugins are installed via git clone or manual copy
**Impact:** Blocks Phase 3 ecosystem growth if distribution is too complex

**Proposed Resolution:**
- Option A: Git-based (current) — simple but requires git knowledge
- Option B: npm/registry — familiar to JS developers, adds dependency
- Option C: Claude Code native — wait for official plugin registry

**Stakeholders Needed:** Claude Code team, early adopters
**Deadline:** Before Phase 3 planning

---

### Q2: Output format extensibility

**Context:** Current output is Markdown only
**Impact:** May limit adoption for teams using other tools (Notion, Jira, Linear)

**Proposed Resolution:**
- Option A: Markdown only (current) — simple, universal
- Option B: Pluggable exporters — more complex, broader reach
- Option C: JSON intermediate — parse-friendly, multiple renderers

**Stakeholders Needed:** Target users, integration partners
**Deadline:** Phase 2

---

## Experiments Needed

### Experiment: Template flexibility

**Hypothesis:** Users want to customize output templates
**Method:** Add template override capability, track usage
**Success Criteria:** >20% of users customize at least one template
**Owner:** Product

### Experiment: Orchestration value

**Hypothesis:** Iterative mode produces better roadmaps than one-shot
**Method:** Compare output quality scores between modes
**Success Criteria:** Orchestrated mode scores 20% higher on completeness
**Owner:** Tech Lead

---

## Parking Lot

- Multi-language support (i18n)
- Integration with project management tools
- AI-powered scope estimation
- Historical roadmap comparison/diff
