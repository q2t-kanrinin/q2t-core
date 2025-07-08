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
