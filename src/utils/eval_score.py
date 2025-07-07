import yaml
from typing import Dict, Any, Optional
from src.models.fold_dsl import FoldDSL, Section
from src.validators.check_structure import validate_links


def load_eval_template(path: str = "docs/tension_eval.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def compute_eval_scores(
    dsl: FoldDSL, eval_template: Dict[str, Any], yaml_path: Optional[str] = None
) -> Dict[str, Any]:
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


if __name__ == "__main__":
    from src.utils.dsl_parser import DSLParser
    yaml_file = "docs/fold_dsl-sample.yaml"
    parser = DSLParser(yaml_file)
    dsl = parser.parse()
    template = load_eval_template()
    scores = compute_eval_scores(dsl, template, yaml_path=yaml_file)
    print("\n=== 評価スコア ===")
    for axis, score in scores.items():
        print(f"{axis}: {score:.2f}")
