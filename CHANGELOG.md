# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/auge2u/ralph-it-up/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/auge2u/ralph-it-up/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/auge2u/ralph-it-up/releases/tag/v1.0.0
