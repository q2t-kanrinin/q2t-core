"""Utility to parse fold_dsl YAML files."""

from __future__ import annotations

import yaml
from ruamel.yaml import YAML
from typing import List, Optional

from src.models.fold_dsl import FoldDSL, Section, Link, Meta, Semantic


class DSLParser:
    """Parser for fold_dsl YAML files preserving comment metadata."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.meta_title: Optional[str] = None
        self.meta_tags: List[str] = []
        self.dsl: Optional[FoldDSL] = None

    def parse(self) -> FoldDSL:
        """Parse the YAML file and return a :class:`FoldDSL` instance."""
        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        comment_lines: List[str] = []
        yaml_start_index = 0
        for idx, line in enumerate(lines):
            if line.lstrip().startswith("#"):
                comment_lines.append(line.strip())
                continue
            if line.strip() == "":
                continue
            yaml_start_index = idx
            break

        self._parse_meta_comments(comment_lines)

        yaml_loader = YAML(typ="safe")
        yaml_lines: List[str] = []
        for line in lines[yaml_start_index:]:
            if line.lstrip().startswith("\u2705"):
                break
            yaml_lines.append(line)
        yaml_content = "".join(yaml_lines)
        data = yaml_loader.load(yaml_content)

        self.dsl = self._map_to_model(data)
        return self.dsl

    def _parse_meta_comments(self, comments: List[str]) -> None:
        yaml_loader = YAML(typ="safe")
        for line in comments:
            text = line.lstrip("#").strip()
            if text.startswith("title:"):
                self.meta_title = text.split("title:", 1)[1].strip()
            elif text.startswith("tags:"):
                tag_text = text.split("tags:", 1)[1].strip()
                try:
                    parsed = yaml_loader.load(tag_text)
                    if isinstance(parsed, list):
                        self.meta_tags = parsed
                    elif parsed is not None:
                        self.meta_tags = [str(parsed)]
                except Exception:
                    self.meta_tags = [tag_text]

    def _parse_section(self, node: dict) -> Section:
        children = [self._parse_section(c) for c in node.get("children", [])]
        return Section(
            id=node["id"],
            name=node["name"],
            description=node.get("description"),
            tension=node.get("tension", 0),
            children=children,
        )

    def _map_to_model(self, data: dict) -> FoldDSL:
        section = self._parse_section(data["section"])
        links = [Link(**l) for l in data.get("links", [])]
        meta = Meta(**data.get("meta", {}))
        semantic = Semantic(**data.get("semantic", {}))

        return FoldDSL(
            id=data.get("id", section.id),
            title=self.meta_title,
            sections=[section],
            links=links,
            meta=meta,
            semantic=semantic,
        )

def load_fold_dsl(path: str) -> dict:
    """Load a fold_dsl file using PyYAML (legacy)."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

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
