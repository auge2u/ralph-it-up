# plugins/ralph-it-up-roadmap/tests/python/test_pattern_exists.py
from validate_quality_gates import QualityGateValidator


def make_gate(path, pattern):
    return {"id": "test", "name": "Test", "check": "pattern_exists",
            "path": path, "pattern": pattern, "severity": "blocker"}


def test_pattern_exists_passes_when_found(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "METRICS_AND_PMF.md").write_text("## North Star Metric\n\nContent.\n")
    gate = make_gate("scopecraft/METRICS_AND_PMF.md", r"North Star Metric")
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is True


def test_pattern_exists_fails_when_not_found(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "METRICS_AND_PMF.md").write_text("## Some Other Section\n")
    gate = make_gate("scopecraft/METRICS_AND_PMF.md", r"North Star Metric")
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False


def test_pattern_exists_fails_when_file_missing(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    gate = make_gate("scopecraft/MISSING.md", r"North Star Metric")
    result = QualityGateValidator(tmp_path, [gate]).validate_all()[0]
    assert result.passed is False
    assert "not found" in result.message
