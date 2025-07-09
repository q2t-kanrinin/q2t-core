# test_dsl_parser.py
from pathlib import Path
from src.models.fold_dsl import FoldDSL
from src.utils.dsl_parser import DSLParser

def test_dslparser_parses_metadata(tmp_path: Path) -> None:
    yaml_text = """\n#title: Sample DSL\n#tags: [foo, bar]\nsection:\n  id: root\n  name: Root\nlinks: []\nmeta:\n  version: "0.1"\n  created: "2025-07-07"\n  author: "tester"\nsemantic:\n  keywords: []\n  themes: []\n"""
    path = tmp_path / "sample.yaml"
    path.write_text(yaml_text, encoding="utf-8")

    parser = DSLParser(str(path))
    dsl: FoldDSL = parser.parse()

    assert isinstance(dsl, FoldDSL)
    assert dsl.title == "Sample DSL"
    assert parser.meta_tags == ["foo", "bar"]
    assert dsl.sections[0].id == "root"
    assert dsl.meta.author == "tester"

    dumped = dsl.model_dump(by_alias=True)
    assert "section" in dumped and dumped["section"][0]["id"] == "root"

def test_dslparser_handles_note_node(tmp_path: Path) -> None:
    yaml_text = """\nsection:\n  id: root\n  name: Root\n  children:\n    - id: child1\n      name: Child1\n    - "@note": sample note\nlinks: []\nmeta:\n  version: "0.1"\n  created: "2025-07-07"\n  author: "tester"\nsemantic:\n  keywords: []\n  themes: []\n"""
    path = tmp_path / "note.yaml"
    path.write_text(yaml_text, encoding="utf-8")

    Parameters
    ----------
    dsl : FoldDSL
        Parsed FoldDSL structure to evaluate.
    eval_template : Dict[str, Any]
        Mapping defining axes and weight settings.
    yaml_path : Optional[str]
        Source YAML path for optional link validation.

    Returns
    -------
    Dict[str, Any]
        Scores keyed by axis name with ``total_score`` included.
    """
    if yaml_path:
        validate_links(dsl, yaml_path)
    def count_depth(section: Section, level: int = 1) -> int:
        if not section.children:
            return level
        return max(count_depth(child, level + 1) for child in section.children)

    def count_breadth(section: Section) -> int:
        total = len(section.children)
        for child in section.children:
            total += count_breadth(child)
        return total

    def count_nodes(section: Section) -> int:
        return 1 + sum(count_nodes(c) for c in section.children)

    section_root = dsl.sections[0]
    total_nodes = count_nodes(section_root)
    depth = count_depth(section_root)
    breadth = count_breadth(section_root) / max(total_nodes - 1, 1)

    keywords = len(dsl.semantic.keywords) if dsl.semantic and dsl.semantic.keywords else 0
    themes = len(dsl.semantic.themes) if dsl.semantic and dsl.semantic.themes else 0
    tension_sum = sum_sections_tension(section_root)

    raw_scores = {
        "depth": depth,
        "breadth": breadth,
        "keywords": keywords,
        "themes": themes,
        "tension_sum": tension_sum,
    }

    results = {}
    total_score = 0.0

    for axis in eval_template["axes"]:
        axis_score = 0.0
        for item in axis["items"]:
            key = item["key"]
            value = raw_scores.get(key, 0)
            weight = item.get("weight", 1.0)
            axis_score += value * weight
        results[axis["axis"]] = axis_score * axis.get("weight", 1.0)
        total_score += results[axis["axis"]]

    results["total_score"] = total_score
    return results


def sum_sections_tension(section: Section) -> int:
    total = section.tension or 0
    for child in section.children:
        total += sum_sections_tension(child)
    return total


def main() -> None:
    """CLI entry point for computing evaluation scores."""
    from src.utils.dsl_parser import DSLParser

    yaml_file = "docs/fold_dsl-sample.yaml"
    parser = DSLParser(yaml_file)
    dsl = parser.parse()
    template = load_eval_template()
    scores = compute_eval_scores(dsl, template, yaml_path=yaml_file)
    print("\n=== 評価スコア ===")
    for axis, score in scores.items():
        print(f"{axis}: {score:.2f}")


__all__ = [
    "load_eval_template",
    "compute_eval_scores",
    "sum_sections_tension",
    "main",
]


if __name__ == "__main__":  # pragma: no cover - CLI usage
    main()
