# plugins/ralph-it-up-roadmap/tests/python/test_pattern_count.py
import pytest
from validate_quality_gates import QualityGateValidator


def make_gate(path, pattern, min=None, max=None):
    g = {"id": "test_gate", "name": "Test", "check": "pattern_count",
         "path": path, "pattern": pattern, "severity": "blocker"}
    if min is not None:
        g["min"] = min
    if max is not None:
        g["max"] = max
    return g


def test_pattern_count_passes_at_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n## Phase 2\n## Phase 3\n")
    gate = make_gate("scopecraft/ROADMAP.md", r"^## Phase \d", min=3)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True
    assert result.actual == 3


def test_pattern_count_fails_below_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n## Phase 2\n")
    gate = make_gate("scopecraft/ROADMAP.md", r"^## Phase \d", min=3)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 2


def test_pattern_count_fails_above_maximum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("[TODO]\n[TODO]\n")
    gate = make_gate("scopecraft/ROADMAP.md", r"\[TODO\]", max=0)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 2


def test_pattern_count_passes_at_zero_when_max_zero(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "file.md").write_text("No placeholders here.\n")
    gate = make_gate("scopecraft/file.md", r"\[TODO\]", max=0)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True
    assert result.actual == 0


def test_pattern_count_fails_when_no_files_found(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    gate = make_gate("scopecraft/NONEXISTENT.md", r"## Phase", min=1)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert "No files found" in result.message


def test_pattern_count_aggregates_across_glob(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "a.md").write_text("[TODO]\n")
    (sc / "b.md").write_text("[TODO]\n[TODO]\n")
    gate = make_gate("scopecraft/*.md", r"\[TODO\]", max=0)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 3
