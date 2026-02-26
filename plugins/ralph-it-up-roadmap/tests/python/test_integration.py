# plugins/ralph-it-up-roadmap/tests/python/test_integration.py
from validate_quality_gates import QualityGateValidator


def test_all_default_gates_pass_on_complete_output(passing_scopecraft):
    v = QualityGateValidator(passing_scopecraft)
    results = v.validate_all()
    failed = [r for r in results if not r.passed]
    assert failed == [], f"Expected all gates to pass, failed: {[r.gate_id for r in failed]}"


def test_all_outputs_exist_gate_fails_on_empty_dir(empty_scopecraft):
    v = QualityGateValidator(empty_scopecraft)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["all_outputs_exist"].passed is False


def test_no_todo_gate_fails_when_placeholder_present(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n[TODO] fill this in\n")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["no_todo_placeholders"].passed is False


def test_unknown_check_type_returns_failed_result(tmp_path):
    gate = {"id": "bad", "name": "Bad", "check": "nonexistent_type",
            "path": "scopecraft/*.md", "severity": "blocker"}
    v = QualityGateValidator(tmp_path, [gate])
    result = v.validate_all()[0]
    assert result.passed is False
    assert "Unknown check type" in result.message


def test_validator_handles_unicode_content(tmp_path):
    """Validator should not crash on files with unicode characters."""
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "METRICS_AND_PMF.md").write_text(
        "## North Star Metric\n\nCafé → Success ✓\n", encoding="utf-8"
    )
    gate = {"id": "metrics_defined", "name": "North Star Metric",
            "check": "pattern_exists", "path": "scopecraft/METRICS_AND_PMF.md",
            "pattern": "North Star Metric", "severity": "blocker"}
    v = QualityGateValidator(tmp_path, [gate])
    result = v.validate_all()[0]
    assert result.passed is True
