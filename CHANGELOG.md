# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-01-27

### Added
- Native Claude Code orchestration mode (`/ralph-it-up-roadmap:roadmap-native`)
- `roadmap-orchestrator` agent for autonomous loop control without external dependencies
- Native bash validation hook (`validate-gates-handler.sh`) - zero dependencies
- JSON output mode for validation hooks (`--json` flag)
- Quiet mode for CI/CD validation (`--quiet` flag)
- `.agent/validation-results.json` output for programmatic gate status

### Changed
- Improved CLAUDE.md accuracy and clarity
- Updated tooling configuration in `.claude/settings.json`

### Documentation
- Added migration guide from ralph-orchestrator to native mode
- Documented all three orchestration modes (one-shot, native, external)

## [1.1.1] - 2026-01-22

### Changed
- Updated ralph-orchestrator compatibility from v2.0.0 to v2.2.0
- Documented all 7 supported backends (claude, gemini, codex, qchat, aider, opencode, copilot)
- Added `ralph plan` and `ralph task` session workflow commands to docs
- Added git SHA pinning installation option for reproducible plugin installs

## [1.1.0] - 2026-01-21

### Added
- Example stories for plugin discovery and quality gate validation

## [1.0.0] - 2024-01-21

### Added
- Initial release of ralph-it-up marketplace
- `ralph-it-up-roadmap` plugin with roadmap generation skill
- One-shot mode (`/ralph-it-up-roadmap:roadmap`)
- Orchestrated loop mode (`/ralph-it-up-roadmap:roadmap-orchestrated`)
- Quality gate validation (`hooks/validate_quality_gates.py`)
- ralph-orchestrator v2.0.0 compatibility with hat-based orchestration
- Templates for all 6 scopecraft output files
- Example outputs in `examples/scopecraft/`

### Documentation
- README with installation and usage instructions
- CLAUDE.md with project architecture and commands
- CONTRIBUTING.md with plugin contribution guidelines

[Unreleased]: https://github.com/auge2u/ralph-it-up/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/auge2u/ralph-it-up/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/auge2u/ralph-it-up/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/auge2u/ralph-it-up/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/auge2u/ralph-it-up/releases/tag/v1.0.0
