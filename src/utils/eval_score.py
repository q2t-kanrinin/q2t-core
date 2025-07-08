"""Compute evaluation scores from a :class:`FoldDSL` instance."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from src.models.fold_dsl import FoldDSL, Section
from src.validators.check_structure import validate_links


def load_eval_template(
    fold_type: str = "default", path: Optional[str] = None
) -> Dict[str, Any]:
    """Load evaluation template either from *path* or by fold_type."""
    if path:
        target = Path(path)
    else:
        target = Path("eval_templates") / f"{fold_type}.yaml"
        if not target.exists():
            target = Path("eval_templates") / "default.yaml"

    with open(target, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def compute_eval_scores(
    dsl: FoldDSL,
    eval_template: Optional[Dict[str, Any]] = None,
    yaml_path: Optional[str] = None,
    fold_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Calculate axis and total scores for a FoldDSL instance.

    Parameters
    ----------
    dsl : FoldDSL
        Parsed FoldDSL structure to evaluate.
    eval_template : Optional[Dict[str, Any]]
        Explicit template mapping. If not provided, load from :func:`load_eval_template`.
    yaml_path : Optional[str]
        Source YAML path for optional link validation.
    fold_type : Optional[str]
        Template name used when loading automatically. If omitted, tries
        ``dsl.meta.fold_type`` or falls back to ``"default"``.

    Returns
    -------
    Dict[str, Any]
        Scores keyed by axis name with ``total_score`` included.
    """
    if yaml_path:
        validate_links(dsl, yaml_path)

    if eval_template is None:
        if fold_type is None:
            fold_type = getattr(dsl.meta, "fold_type", None)
            if fold_type is None:
                for tag in getattr(dsl.meta, "tags", []):
                    if tag.startswith("type:"):
                        fold_type = tag.split(":", 1)[1]
                        break
        fold_type = fold_type or "default"
        eval_template = load_eval_template(fold_type)

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

    keywords = (
        len(dsl.semantic.keywords) if dsl.semantic and dsl.semantic.keywords else 0
    )
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
    scores = compute_eval_scores(dsl, yaml_path=yaml_file)
    print("\n=== 評価スコア ===")
    for axis, score in scores.items():
        print(f"{axis}: {score:.2f}")
