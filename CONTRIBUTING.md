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

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0): Breaking changes to plugin API or output format
- **MINOR** (0.x.0): New features, new plugins, backwards-compatible additions
- **PATCH** (0.0.x): Bug fixes, documentation updates, minor improvements

### Version locations

Versions are tracked in two files that must stay in sync:

- `plugins/ralph-it-up-roadmap/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

### Bumping versions

Use the bump script to update all version references:

```bash
# Bump to a new version
./scripts/bump-version.sh 1.1.0

# Bump and create a git tag
./scripts/bump-version.sh 1.1.0 --tag
```

The script updates:
- Both `plugin.json` and `marketplace.json`
- `CHANGELOG.md` (moves Unreleased to new version with today's date)

### Release process

1. Ensure all changes are committed
2. Update `CHANGELOG.md` with release notes under `[Unreleased]`
3. Run `./scripts/bump-version.sh <version> --tag`
4. Review changes: `git diff`
5. Commit: `git add -A && git commit -m "Release v<version>"`
6. Push: `git push && git push --tags`
7. Create GitHub release from the tag

### Changelog format

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Removed
- Removed features
```
