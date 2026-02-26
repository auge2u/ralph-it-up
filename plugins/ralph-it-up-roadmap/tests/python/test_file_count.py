# plugins/ralph-it-up-roadmap/tests/python/test_file_count.py
from validate_quality_gates import QualityGateValidator

GATE = {
    "id": "all_outputs_exist",
    "name": "All required outputs exist",
    "check": "file_count",
    "path": "scopecraft/*.md",
    "expect": 6,
    "severity": "blocker",
}


def test_file_count_passes_with_exactly_six(passing_scopecraft):
    v = QualityGateValidator(passing_scopecraft, [GATE])
    result = v.validate_all()[0]
    assert result.passed is True
    assert result.actual == 6


def test_file_count_fails_with_five_files(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    for i in range(5):
        (sc / f"file{i}.md").write_text("content")
    v = QualityGateValidator(tmp_path, [GATE])
    result = v.validate_all()[0]
    assert result.passed is False
    assert result.actual == 5


def test_file_count_fails_with_empty_dir(empty_scopecraft):
    v = QualityGateValidator(empty_scopecraft, [GATE])
    result = v.validate_all()[0]
    assert result.passed is False
    assert result.actual == 0


def test_file_count_fails_with_seven_files(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    for i in range(7):
        (sc / f"file{i}.md").write_text("content")
    v = QualityGateValidator(tmp_path, [GATE])
    result = v.validate_all()[0]
    assert result.passed is False
    assert result.actual == 7


def test_file_count_result_has_expected_set(passing_scopecraft):
    v = QualityGateValidator(passing_scopecraft, [GATE])
    result = v.validate_all()[0]
    assert result.expected == "6"
