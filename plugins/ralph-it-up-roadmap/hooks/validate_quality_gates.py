#!/usr/bin/env python3
"""
Quality Gates Validator for ralph-it-up-roadmap

Validates scopecraft outputs against quality gate definitions.
Can be run standalone or as a ralph-orchestrator hook.

Usage:
    python validate_quality_gates.py [--config ralph.yml] [--output-dir scopecraft]

Exit codes:
    0 - All gates passed
    1 - Blocker gates failed
    2 - Warning gates failed (but no blockers)
"""

import argparse
import glob
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class GateResult:
    """Result of a quality gate check."""
    gate_id: str
    name: str
    passed: bool
    severity: str
    message: str
    actual: Optional[int] = None
    expected: Optional[str] = None


class QualityGateValidator:
    """Validates outputs against quality gate definitions."""

    DEFAULT_GATES = [
        {
            "id": "all_outputs_exist",
            "name": "All required outputs exist",
            "check": "file_count",
            "path": "scopecraft/*.md",
            "expect": 6,
            "severity": "blocker"
        },
        {
            "id": "phases_in_range",
            "name": "Roadmap has 3-5 phases",
            "check": "pattern_count",
            "path": "scopecraft/ROADMAP.md",
            "pattern": r"^## Phase \d",
            "min": 3,
            "max": 5,
            "severity": "blocker"
        },
        {
            "id": "stories_have_acceptance_criteria",
            "name": "Stories have acceptance criteria",
            "check": "pattern_count",
            "path": "scopecraft/EPICS_AND_STORIES.md",
            "pattern": r"Acceptance Criteria",
            "min": 5,
            "severity": "blocker"
        },
        {
            "id": "risks_documented",
            "name": "Risk register has entries",
            "check": "pattern_count",
            "path": "scopecraft/RISKS_AND_DEPENDENCIES.md",
            "pattern": r"\| .+ \| (Technical|Product|GTM)",
            "min": 3,
            "severity": "blocker"
        },
        {
            "id": "no_todo_placeholders",
            "name": "No TODO placeholders remain",
            "check": "pattern_count",
            "path": "scopecraft/*.md",
            "pattern": r"\[TODO\]|\[TBD\]|\[PLACEHOLDER\]",
            "max": 0,
            "severity": "blocker"
        },
        {
            "id": "metrics_defined",
            "name": "North star metric defined",
            "check": "pattern_exists",
            "path": "scopecraft/METRICS_AND_PMF.md",
            "pattern": r"North Star Metric",
            "severity": "blocker"
        }
    ]

    def __init__(self, base_dir: Path, gates: list = None):
        self.base_dir = Path(base_dir)
        self.gates = gates or self.DEFAULT_GATES

    def validate_all(self) -> list[GateResult]:
        """Run all quality gate checks."""
        results = []
        for gate in self.gates:
            result = self._check_gate(gate)
            results.append(result)
        return results

    def _check_gate(self, gate: dict) -> GateResult:
        """Check a single quality gate."""
        check_type = gate.get("check")

        if check_type == "file_count":
            return self._check_file_count(gate)
        elif check_type == "min_lines":
            return self._check_min_lines(gate)
        elif check_type == "pattern_count":
            return self._check_pattern_count(gate)
        elif check_type == "pattern_exists":
            return self._check_pattern_exists(gate)
        else:
            return GateResult(
                gate_id=gate.get("id", "unknown"),
                name=gate.get("name", "Unknown gate"),
                passed=False,
                severity=gate.get("severity", "warning"),
                message=f"Unknown check type: {check_type}"
            )

    def _check_file_count(self, gate: dict) -> GateResult:
        """Check that expected number of files exist."""
        pattern = self.base_dir / gate["path"]
        files = glob.glob(str(pattern))
        count = len(files)
        expected = gate.get("expect", 0)
        passed = count == expected

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=f"Found {count} files" if passed else f"Expected {expected} files, found {count}",
            actual=count,
            expected=str(expected)
        )

    def _check_min_lines(self, gate: dict) -> GateResult:
        """Check that file has minimum number of lines."""
        file_path = self.base_dir / gate["path"]

        if not file_path.exists():
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"File not found: {gate['path']}"
            )

        with open(file_path, "r") as f:
            lines = len(f.readlines())

        min_lines = gate.get("min", 0)
        passed = lines >= min_lines

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=f"File has {lines} lines" if passed else f"Expected min {min_lines} lines, found {lines}",
            actual=lines,
            expected=f">= {min_lines}"
        )

    def _check_pattern_count(self, gate: dict) -> GateResult:
        """Check pattern occurrence count against min/max."""
        pattern_path = self.base_dir / gate["path"]
        files = glob.glob(str(pattern_path))

        if not files:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"No files found matching: {gate['path']}"
            )

        regex = re.compile(gate["pattern"], re.MULTILINE)
        total_count = 0

        for file_path in files:
            with open(file_path, "r") as f:
                content = f.read()
                matches = regex.findall(content)
                total_count += len(matches)

        min_count = gate.get("min")
        max_count = gate.get("max")

        passed = True
        expected_parts = []

        if min_count is not None:
            if total_count < min_count:
                passed = False
            expected_parts.append(f">= {min_count}")

        if max_count is not None:
            if total_count > max_count:
                passed = False
            expected_parts.append(f"<= {max_count}")

        expected = " and ".join(expected_parts) if expected_parts else "any"

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=f"Found {total_count} matches" if passed else f"Expected {expected}, found {total_count}",
            actual=total_count,
            expected=expected
        )

    def _check_pattern_exists(self, gate: dict) -> GateResult:
        """Check that pattern exists at least once."""
        file_path = self.base_dir / gate["path"]

        if not file_path.exists():
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"File not found: {gate['path']}"
            )

        with open(file_path, "r") as f:
            content = f.read()

        regex = re.compile(gate["pattern"], re.MULTILINE)
        match = regex.search(content)
        passed = match is not None

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message="Pattern found" if passed else f"Pattern not found: {gate['pattern']}"
        )


def load_gates_from_config(config_path: Path) -> list:
    """Load quality gates from ralph.yml config."""
    if not HAS_YAML:
        print("Warning: PyYAML not installed, using default gates", file=sys.stderr)
        return None

    if not config_path.exists():
        return None

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config.get("quality_gates")


def print_results(results: list[GateResult], verbose: bool = False) -> tuple[int, int]:
    """Print validation results and return counts."""
    blockers_failed = 0
    warnings_failed = 0

    print("\n" + "=" * 60)
    print("QUALITY GATE VALIDATION RESULTS")
    print("=" * 60 + "\n")

    for result in results:
        if result.passed:
            status = "✓ PASS"
            color = "\033[92m"  # Green
        elif result.severity == "blocker":
            status = "✗ FAIL"
            color = "\033[91m"  # Red
            blockers_failed += 1
        else:
            status = "⚠ WARN"
            color = "\033[93m"  # Yellow
            warnings_failed += 1

        reset = "\033[0m"
        print(f"{color}{status}{reset} [{result.gate_id}] {result.name}")

        if verbose or not result.passed:
            print(f"       {result.message}")
        print()

    # Summary
    total = len(results)
    passed = total - blockers_failed - warnings_failed

    print("-" * 60)
    print(f"Total: {total} | Passed: {passed} | Blockers: {blockers_failed} | Warnings: {warnings_failed}")
    print("-" * 60)

    if blockers_failed > 0:
        print("\n❌ QUALITY GATES FAILED - Cannot issue LOOP_COMPLETE")
    elif warnings_failed > 0:
        print("\n⚠️  QUALITY GATES PASSED WITH WARNINGS - Can issue LOOP_COMPLETE")
    else:
        print("\n✅ ALL QUALITY GATES PASSED - Ready for LOOP_COMPLETE")

    return blockers_failed, warnings_failed


def generate_markdown_report(results: list[GateResult]) -> str:
    """Generate markdown report for scratchpad."""
    lines = [
        "## Quality Gate Status",
        "",
        "| Status | Gate | Message |",
        "|--------|------|---------|"
    ]

    for result in results:
        if result.passed:
            status = "✅"
        elif result.severity == "blocker":
            status = "❌"
        else:
            status = "⚠️"

        lines.append(f"| {status} | {result.name} | {result.message} |")

    blockers = sum(1 for r in results if not r.passed and r.severity == "blocker")

    lines.extend([
        "",
        f"**Blockers remaining: {blockers}**",
        ""
    ])

    if blockers > 0:
        lines.append("⛔ Cannot issue LOOP_COMPLETE until all blockers pass.")
    else:
        lines.append("✅ Ready to issue LOOP_COMPLETE.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate quality gates for ralph-it-up-roadmap")
    parser.add_argument("--config", "-c", default="ralph.yml", help="Path to ralph.yml config")
    parser.add_argument("--output-dir", "-o", default=".", help="Base directory for outputs")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all gate details")
    parser.add_argument("--markdown", "-m", action="store_true", help="Output markdown report")
    parser.add_argument("--scratchpad", "-s", help="Append results to scratchpad file")
    args = parser.parse_args()

    # Load gates from config or use defaults
    gates = load_gates_from_config(Path(args.config))

    # Run validation
    validator = QualityGateValidator(Path(args.output_dir), gates)
    results = validator.validate_all()

    if args.markdown:
        print(generate_markdown_report(results))
    else:
        blockers, warnings = print_results(results, args.verbose)

        # Optionally append to scratchpad
        if args.scratchpad:
            scratchpad_path = Path(args.scratchpad)
            if scratchpad_path.exists():
                with open(scratchpad_path, "a") as f:
                    f.write("\n\n")
                    f.write(generate_markdown_report(results))
                print(f"\nResults appended to {args.scratchpad}")

        # Exit code
        if blockers > 0:
            sys.exit(1)
        elif warnings > 0:
            sys.exit(2)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
