# plugins/ralph-it-up-roadmap/tests/python/test_new_gates.py
from validate_quality_gates import QualityGateValidator


def test_roadmap_has_content_passes_with_fifty_lines(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("\n" * 49 + "line 50\n", encoding="utf-8")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["roadmap_has_content"].passed is True


def test_roadmap_has_content_fails_with_stub(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "ROADMAP.md").write_text("## Phase 1\n## Phase 2\n## Phase 3\n", encoding="utf-8")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["roadmap_has_content"].passed is False


def test_open_questions_populated_passes_with_section(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "OPEN_QUESTIONS.md").write_text(
        "# Open Questions\n\n## Question 1\n\nDetails.\n", encoding="utf-8"
    )
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["open_questions_populated"].passed is True


def test_open_questions_populated_fails_with_empty_file(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    (sc / "OPEN_QUESTIONS.md").write_text("# Open Questions\n", encoding="utf-8")
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["open_questions_populated"].passed is False


def test_open_questions_populated_fails_when_file_missing(tmp_path):
    sc = tmp_path / "scopecraft"
    sc.mkdir()
    v = QualityGateValidator(tmp_path)
    results = {r.gate_id: r for r in v.validate_all()}
    assert results["open_questions_populated"].passed is False
