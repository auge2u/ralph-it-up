# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- `validate_quality_gates.py`: `--markdown` flag now exits non-zero when blocker
  gates fail; previously always exited 0 regardless of gate status
- `validate_quality_gates.py`: warn to stderr when `--scratchpad` file not found
  instead of silently skipping the append
- `validate-gates-handler.sh`: `--output-dir` now errors if no value is provided
- `SKILL.md`: quality gate checklist now matches the 8 implemented gates; removed
  phantom `epics_have_stories`, `vision_not_empty`, `no_empty_brackets` entries
  and added `roadmap_has_content` and `open_questions_populated`

### Changed
- `validate_quality_gates.py`: added `from __future__ import annotations` for
  Python 3.8/3.9 compatibility; clarified `--output-dir` semantics in docstring
- CI: upgraded `actions/checkout` to v5 in both jobs
- CI: pinned `bats-core` install to tag `v1.11.0` for reproducibility
- CI: added pip dependency caching via `setup-python cache: pip`
- CI: enabled coverage reporting (`--cov`) in pytest step

### Tests
- Added `test_markdown_mode_exits_nonzero_on_blocker_failure` (pytest)
- Added `json mode exits 1 when gates fail` (bats)

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
