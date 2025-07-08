"""Utility script for evaluating a ``FoldDSL`` against a scoring config.

This module exposes :class:`FoldEvaluator` which loads a FoldDSL YAML file
and an evaluation configuration to compute various scores.  It was
originally saved with a ``.yaml`` extension but actually contains Python
code; the file has been renamed to better reflect its contents.
"""

import math
from src.models.fold_dsl import FoldDSL
from src.utils.dsl_parser import DSLParser
from src.utils.eval_utils import load_eval_config


class FoldEvaluator:
    def __init__(self, fold_path: str, config_path: str):
        self.dsl: FoldDSL = DSLParser(fold_path).parse()
        self.config = load_eval_config(config_path)

    def compute(self) -> dict:
        result = {}
        total = 0.0

        for axis in self.config["axes"]:
            axis_score = 0.0
            for item in axis["items"]:
                key = item["key"]
                weight = item["weight"]
                value = self._extract_metric(key)
                axis_score += value * weight

            result[axis["key"]] = round(axis_score, 2)
            total += axis_score * axis["weight"]

        result["total_score"] = round(total, 2)
        return result

    def _extract_metric(self, key: str) -> float:
        if key == "depth":
            return self._compute_depth()
        elif key == "contradiction_links":
            return self._count_links_by_type("contradiction")
        elif key == "bridge_resolutions":
            return self._count_links_by_type("resolution")
        elif key == "tension_stddev":
            return self._tension_stddev()
        elif key == "keywords":
            return float(len(self.dsl.semantic.keywords or []))
        elif key == "themes":
            return float(len(self.dsl.semantic.themes or []))
        return 0.0

    def _compute_depth(self) -> int:
        def depth(node, level=1):
            if not node.children:
                return level
            return max(depth(child, level + 1) for child in node.children)
        return depth(self.dsl.sections[0])

    def _count_links_by_type(self, link_type: str) -> int:
        return sum(1 for link in self.dsl.links if link.type == link_type)

    def _tension_stddev(self) -> float:
        tensions = []
        def collect(node):
            tensions.append(node.tension or 0)
            for c in node.children:
                collect(c)
        collect(self.dsl.sections[0])
        if not tensions:
            return 0.0
        mean = sum(tensions) / len(tensions)
        var = sum((t - mean) ** 2 for t in tensions) / len(tensions)
        return math.sqrt(var)


if __name__ == "__main__":
    import sys
    from pprint import pprint

    fold_path = "docs/fold_dsl-sample.yaml"
    config_path = "docs/refutation_eval.py"

    evaluator = FoldEvaluator(fold_path, config_path)
    scores = evaluator.compute()

    print("=== 評価スコア ===")
    for k, v in scores.items():
        print(f"{k}: {v}")
