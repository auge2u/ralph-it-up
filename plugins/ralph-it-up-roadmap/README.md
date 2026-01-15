# ralph-it-up-roadmap

Generate a full-scope product roadmap from an existing repository by scanning docs/PRDs and legacy tasks.

**ralph-orchestrator compatible** — works standalone or with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) for autonomous iteration.

## Commands

### Roadmap (one-shot)
```txt
/ralph-it-up-roadmap:roadmap
```

### Roadmap (orchestrated loop)
```txt
/ralph-it-up-roadmap:roadmap-orchestrated
```

## What it produces

Creates a `./scopecraft/` directory containing:
- Vision + definition of "next major stage"
- Roadmap phases with outcomes/KRs
- Epics & stories with acceptance criteria
- Risk register + dependencies
- PMF metrics + instrumentation outline
- Open questions / decisions needed

## Examples

See `examples/scopecraft/` for sample outputs demonstrating expected format and detail level.

## ralph-orchestrator Integration

For autonomous iteration with [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator):

### Quick Start

```bash
# Install ralph-orchestrator
pip install ralph-orchestrator

# Copy templates to your project
cp templates/PROMPT.md ./PROMPT.md
cp templates/ralph.yml ./ralph.yml
mkdir -p .agent && cp templates/scratchpad.md ./.agent/scratchpad.md

# Run orchestrated roadmap generation
ralph run -a claude
```

### Configuration

Edit `ralph.yml` to adjust:
- `max_iterations` — default 15, increase for complex projects
- `max_runtime` — default 1 hour
- `max_cost` — default $25 USD ceiling
- `checkpoint_interval` — git commits every N iterations

### Completion Promise

The skill uses `LOOP_COMPLETE` as its completion marker, compatible with ralph-orchestrator defaults.

### Scratchpad

Progress is tracked in `.agent/scratchpad.md` between iterations, enabling:
- Incremental improvement (not full rewrites)
- Recovery from interruptions
- Visibility into agent progress
