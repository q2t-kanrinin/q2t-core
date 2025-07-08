"""Example script for parsing and displaying FoldDSL YAML files."""

from src.utils.dsl_parser import DSLParser  # ✅ 外部化されたクラスを利用
from src.models.fold_dsl import FoldDSL, Section


def print_section_tree(section: Section, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {section.name} (ID: {section.id}, tension: {section.tension})")
    for child in section.children:
        print_section_tree(child, level + 1)


if __name__ == "__main__":
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl: FoldDSL = parser.parse()

    print(f"\n=== Meta ===")
    print(f"Title: {dsl.title}")
    print(f"Tags: {parser.meta_tags}")

    print("\n=== Fold構造 ===")
    print_section_tree(dsl.sections[0])

    print("\n=== Bridgeリンク ===")
    for link in dsl.links:
        print(f"{link.source} -> {link.target} (type: {link.type}, weight: {link.weight})")

    print("\n=== Semantic ===")
    print(dsl.semantic.model_dump())
