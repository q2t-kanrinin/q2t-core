from pathlib import Path

from src.utils.dsl_parser import DSLParser
from src.utils.eval_score import load_eval_template, compute_eval_scores


def test_compute_eval_scores(tmp_path: Path) -> None:
    sample_src = Path("docs/fold_dsl-sample.yaml")
    raw = sample_src.read_text(encoding="utf-8")
    if "✅" in raw:
        raw = raw.split("✅", 1)[0]
    sample_tmp = tmp_path / "sample.yaml"
    sample_tmp.write_text(raw, encoding="utf-8")

    parser = DSLParser(str(sample_tmp))
    dsl = parser.parse()

    template = load_eval_template("docs/tension_eval.yaml")
    scores = compute_eval_scores(dsl, template, yaml_path=str(sample_tmp))

    assert "total_score" in scores
    assert "構造性" in scores
    assert "意味密度" in scores
    assert "テンション分布" in scores

import pytest
from src.models.fold_dsl import FoldDSL, Section, Meta, Semantic
from src.utils.eval_score import sum_sections_tension


def test_compute_eval_scores_values() -> None:
    root = Section(id="root", name="Root", tension=1, children=[Section(id="child", name="Child", tension=2)])
    meta = Meta(version="0.1", created="2025-01-01", author="tester")
    semantic = Semantic(keywords=["A", "B"], themes=["T1"])
    dsl = FoldDSL(id="x", sections=[root], links=[], meta=meta, semantic=semantic)

    template = load_eval_template("docs/tension_eval.yaml")
    scores = compute_eval_scores(dsl, template)

    assert scores["構造性"] == pytest.approx(1.5)
    assert scores["意味密度"] == pytest.approx(1.6)
    assert scores["テンション分布"] == pytest.approx(3.0)
    assert scores["total_score"] == pytest.approx(6.1)


def test_sum_sections_tension() -> None:
    root = Section(id="root", name="Root", tension=2, children=[Section(id="child", name="Child", tension=1)])
    assert sum_sections_tension(root) == 3
