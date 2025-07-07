from pathlib import Path
from src.models.fold_dsl import FoldDSL
from src.utils.dsl_parser import DSLParser


def test_dslparser_parses_metadata(tmp_path: Path) -> None:
    yaml_text = """\
#title: Sample DSL
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

    parser = DSLParser(str(path))
    dsl: FoldDSL = parser.parse()

    assert isinstance(dsl, FoldDSL)
    assert dsl.title == "Sample DSL"
    assert parser.meta_tags == ["foo", "bar"]
    assert dsl.sections[0].id == "root"
    assert dsl.meta.author == "tester"
