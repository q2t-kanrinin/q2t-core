"""Utilities for loading FoldDSL YAML files."""

import yaml
from typing import Dict, Tuple

from ruamel.yaml import YAML

from src.models.fold_dsl import FoldDSL

def load_fold_dsl(path: str) -> dict:
    """Load a FoldDSL YAML file and return the raw dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def parse_fold_dsl(path: str) -> Tuple[FoldDSL, Dict[str, str]]:
    """Parse a FoldDSL YAML file preserving comments.

    Parameters
    ----------
    path: str
        Path to the YAML file.

    Returns
    -------
    Tuple[FoldDSL, Dict[str, str]]
        The ``FoldDSL`` object along with a mapping from top level keys to their
        comments (if any).
    """
    yaml_parser = YAML()
    with open(path, "r", encoding="utf-8") as f:
        data = yaml_parser.load(f)

    comments: Dict[str, str] = {}
    ca = getattr(data, "ca", None)
    if ca and getattr(ca, "items", None):
        for key, val in ca.items.items():
            if val:
                token = val[2] or val[0]
                if token:
                    comments[key] = token.value.lstrip("#").strip()

    dsl = FoldDSL(**data)
    return dsl, comments

def print_section_tree(section: dict, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {section['name']} (ID: {section['id']}, tension: {section.get('tension',0)})")
    # 子要素がある場合は再帰
    for child in section.get("children", []):
        print_section_tree(child, level + 1)

if __name__ == "__main__":
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()

    section = dsl.sections[0]
    print("=== Fold構造 ===")
    print_section_tree(section.model_dump())

    print("\n=== Bridgeリンク ===")
    for link in dsl.links:
        print(f"{link.source} -> {link.target} (type: {link.type}, weight: {link.weight})")

    print("\n=== Semantic ===")
    print(dsl.semantic.model_dump())

    if parser.meta_title:
        print(f"\nMeta Title: {parser.meta_title}")
    if parser.meta_tags:
        print(f"Meta Tags: {parser.meta_tags}")
