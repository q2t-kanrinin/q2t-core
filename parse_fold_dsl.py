"""Utility functions for loading and parsing FoldDSL YAML files."""

from typing import List

import yaml

from src.models.fold_dsl import FoldDSL

def load_fold_dsl(path: str) -> dict:
    """Load a FoldDSL YAML file and return it as a ``dict``."""

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def parse_fold_dsl(path: str) -> FoldDSL:
    """Parse a FoldDSL YAML file and return a :class:`FoldDSL` instance.

    The function also supports Zettel style comments at the top of the file:

    ``#title`` and ``#tags``. These values are injected into the resulting
    :class:`FoldDSL` object if not already present in the YAML body.
    """

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    title: str | None = None
    tags: List[str] | None = None
    yaml_lines: list[str] = []

    for line in lines:
        if line.startswith("#title:"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("#tags:"):
            tag_part = line.split(":", 1)[1].strip()
            if tag_part.startswith("[") and tag_part.endswith("]"):
                tag_part = tag_part[1:-1]
            tags = [t.strip() for t in tag_part.split(",") if t.strip()]
        else:
            yaml_lines.append(line)

    data = yaml.safe_load("".join(yaml_lines)) or {}

    if title is not None:
        data.setdefault("title", title)
    if tags is not None:
        data.setdefault("meta", {}).setdefault("tags", tags)

    return FoldDSL(**data)

def print_section_tree(section: dict, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {section['name']} (ID: {section['id']}, tension: {section.get('tension',0)})")
    # 子要素がある場合は再帰
    for child in section.get("children", []):
        print_section_tree(child, level + 1)

if __name__ == "__main__":
    dsl = load_fold_dsl("docs/fold_dsl-sample.yaml")
    
    section = dsl.get("section")
    print("=== Fold構造 ===")
    print_section_tree(section)

    print("\n=== Bridgeリンク ===")
    links = dsl.get("links", [])
    for link in links:
        print(f"{link['source']} -> {link['target']} (type: {link['type']}, weight: {link['weight']})")

    print("\n=== Semantic ===")
    semantic = dsl.get("semantic", {})
    print(semantic)
