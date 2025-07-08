from pathlib import Path

from src.utils.dsl_parser import DSLParser
from src.utils.ast_builder import ASTBuilder


def test_ast_builder_parse_dsl(tmp_path: Path) -> None:
    yaml_text = """
section:
  id: root
  name: Root
  children:
    - id: child
      name: Child
links:
  - source: root
    target: child
    type: assoc
    weight: 0.6
meta:
  version: "0.1"
  created: "2025-01-01"
  author: tester
semantic:
  keywords: []
  themes: []
"""
    path = tmp_path / "sample.yaml"
    path.write_text(yaml_text, encoding="utf-8")

    parser = DSLParser(str(path))
    dsl = parser.parse()

    nodes, edges = ASTBuilder.parse_dsl(dsl)

    node_map = {n.id: n for n in nodes}
    assert set(node_map.keys()) == {"root", "child"}
    assert node_map["root"].children == ["child"]
    assert node_map["child"].parent == "root"
    assert len(edges) == 1
    edge = edges[0]
    assert edge.source == "root"
    assert edge.target == "child"
    assert edge.label == "assoc"
    assert edge.weight == 0.6
