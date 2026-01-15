# ralph-it-up-roadmap

Generate a full-scope product roadmap from an existing repository by scanning docs/PRDs and legacy tasks.

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
- Vision + definition of “next major stage”
- Roadmap phases with outcomes/KRs
- Epics & stories with acceptance criteria
- Risk register + dependencies
- PMF metrics + instrumentation outline
- Open questions / decisions needed