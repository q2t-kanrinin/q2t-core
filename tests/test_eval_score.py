from pathlib import Path

from src.utils.dsl_parser import DSLParser
from src.utils.eval_score import compute_eval_scores


def test_compute_eval_scores(tmp_path: Path) -> None:
    sample_src = Path("docs/fold_dsl-sample.yaml")
    raw = sample_src.read_text(encoding="utf-8")
    if "✅" in raw:
        raw = raw.split("✅", 1)[0]
    sample_tmp = tmp_path / "sample.yaml"
    sample_tmp.write_text(raw, encoding="utf-8")

    parser = DSLParser(str(sample_tmp))
    dsl = parser.parse()

    scores_default = compute_eval_scores(dsl, yaml_path=str(sample_tmp))
    scores_flat = compute_eval_scores(dsl, fold_type="flat", yaml_path=str(sample_tmp))

    assert "total_score" in scores_default
    assert "total_score" in scores_flat
    assert scores_default["total_score"] != scores_flat["total_score"]
