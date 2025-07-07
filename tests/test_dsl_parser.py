from src.utils.dsl_parser import DSLParser
from src.models.fold_dsl import FoldDSL


def test_dsl_parser_extracts_metadata(tmp_path):
    yaml_text = """#title: Sample DSL
#tags: [foo, bar]
section:
  id: root
  name: Root
links: []
meta:
  version: "0.1"
  created: "2025-07-07"
  author: "tester"
semantic:
  keywords: []
  themes: []
"""
    path = tmp_path / "sample.yaml"
    path.write_text(yaml_text, encoding="utf-8")

    parser = DSLParser()
    dsl = parser.parse(str(path))

    assert isinstance(dsl, FoldDSL)
    assert dsl.title == "Sample DSL"
    assert dsl.tags == ["foo", "bar"]
    assert dsl.sections[0].id == "root"
