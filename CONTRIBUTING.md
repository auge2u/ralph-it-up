# Contributing

## Adding a new plugin
1) Create a folder under `plugins/<plugin-name>/`
2) Add `plugins/<plugin-name>/.claude-plugin/plugin.json`
3) Add commands under `plugins/<plugin-name>/commands/`
4) Add skills under `plugins/<plugin-name>/skills/`
5) Register the plugin in `.claude-plugin/marketplace.json`

## Quality bar
- Commands should be deterministic and file-output driven.
- Skills should define clear completion criteria.
- Prefer outcomes/KRs over feature lists.
- Keep roadmap phases to 3–5 max.
