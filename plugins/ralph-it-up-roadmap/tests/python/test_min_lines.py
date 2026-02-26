# plugins/ralph-it-up-roadmap/tests/python/test_min_lines.py
from validate_quality_gates import QualityGateValidator


def make_gate(path, min_lines):
    return {"id": "test", "name": "Test", "check": "min_lines",
            "path": path, "min": min_lines, "severity": "blocker"}


def test_min_lines_passes_at_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("\n" * 49 + "line 50\n")
    gate = make_gate("scopecraft/ROADMAP.md", 50)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True
    assert result.actual == 50


def test_min_lines_fails_below_minimum(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("short\n")
    gate = make_gate("scopecraft/ROADMAP.md", 50)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert result.actual == 1


def test_min_lines_fails_when_file_missing(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    gate = make_gate("scopecraft/MISSING.md", 50)
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert "not found" in result.message
