"""Parser entrypoint for FoldDSL YAML files (Zettel対応版)."""

import yaml
from typing import Dict
from ruamel.yaml import YAML

from src.models.fold_dsl import FoldDSL, Section, Link, Meta, Semantic


class DSLParser:
    """Parser for fold_dsl YAML files preserving comment metadata."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.meta_title = None
        self.meta_tags = []
        self.dsl: FoldDSL | None = None

    def parse(self) -> FoldDSL:
        """Parse YAML and return FoldDSL object."""
        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        comments, yaml_start = [], 0
        for idx, line in enumerate(lines):
            if line.strip().startswith("#"):
                comments.append(line.strip())
            elif line.strip():
                yaml_start = idx
                break

        self._parse_meta_comments(comments)
        yaml_body = "".join(lines[yaml_start:])
        yaml_loader = YAML(typ="safe")
        data = yaml_loader.load(yaml_body)

        self.dsl = self._map_to_model(data)
        return self.dsl

    def _parse_meta_comments(self, comments: list[str]) -> None:
        loader = YAML(typ="safe")
        for line in comments:
            txt = line.lstrip("#").strip()
            if txt.startswith("title:"):
                self.meta_title = txt.split("title:", 1)[1].strip()
            elif txt.startswith("tags:"):
                raw = txt.split("tags:", 1)[1].strip()
                try:
                    tags = loader.load(raw)
                    self.meta_tags = tags if isinstance(tags, list) else [str(tags)]
                except Exception:
                    self.meta_tags = [raw]

    def _parse_section(self, node: dict) -> Section:
        return Section(
            id=node["id"],
            name=node["name"],
            description=node.get("description"),
            tension=node.get("tension", 0),
            children=[self._parse_section(c) for c in node.get("children", [])],
        )

    def _map_to_model(self, data: dict) -> FoldDSL:
        section = self._parse_section(data["section"])
        return FoldDSL(
            id=data.get("id", section.id),
            title=self.meta_title,
            sections=[section],
            links=[Link(**l) for l in data.get("links", [])],
            meta=Meta(**data.get("meta", {})),
            semantic=Semantic(**data.get("semantic", {})),
        )


def load_fold_dsl(path: str) -> dict:
    """Legacy fallback: Load FoldDSL YAML as raw dict."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def print_section_tree(section: dict, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {section['name']} (ID: {section['id']}, tension: {section.get('tension', 0)})")
    for child in section.get("children", []):
        print_section_tree(child, level + 1)


if __name__ == "__main__":
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()

    print("=== Fold構造 ===")
    print_section_tree(dsl.sections[0].model_dump())

    print("\n=== Bridgeリンク ===")
    for link in dsl.links:
        print(f"{link.source} -> {link.target} (type: {link.type}, weight: {link.weight})")

    print("\n=== Semantic ===")
    print(dsl.semantic.model_dump())

    if parser.meta_title:
        print(f"\nMeta Title: {parser.meta_title}")
    if parser.meta_tags:
        print(f"Meta Tags: {parser.meta_tags}")
