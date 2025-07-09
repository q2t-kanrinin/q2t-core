# test_dsl_parser.py
from pathlib import Path
from src.models.fold_dsl import FoldDSL
from src.utils.dsl_parser import DSLParser

def test_dslparser_parses_metadata(tmp_path: Path) -> None:
    yaml_text = """\n#title: Sample DSL\n#tags: [foo, bar]\nsection:\n  id: root\n  name: Root\nlinks: []\nmeta:\n  version: "0.1"\n  created: "2025-07-07"\n  author: "tester"\nsemantic:\n  keywords: []\n  themes: []\n"""
    path = tmp_path / "sample.yaml"
    path.write_text(yaml_text, encoding="utf-8")

    parser = DSLParser(str(path))
    dsl: FoldDSL = parser.parse()

    assert isinstance(dsl, FoldDSL)
    assert dsl.title == "Sample DSL"
    assert parser.meta_tags == ["foo", "bar"]
    assert dsl.sections[0].id == "root"
    assert dsl.meta.author == "tester"

    dumped = dsl.model_dump(by_alias=True)
    assert "section" in dumped and dumped["section"][0]["id"] == "root"

def test_dslparser_handles_note_node(tmp_path: Path) -> None:
    yaml_text = """\nsection:\n  id: root\n  name: Root\n  children:\n    - id: child1\n      name: Child1\n    - "@note": sample note\nlinks: []\nmeta:\n  version: "0.1"\n  created: "2025-07-07"\n  author: "tester"\nsemantic:\n  keywords: []\n  themes: []\n"""
    path = tmp_path / "note.yaml"
    path.write_text(yaml_text, encoding="utf-8")

    parser = DSLParser(str(path))
    dsl = parser.parse()

    root_section = dsl.sections[0]
    assert len(root_section.notes) == 1
    assert root_section.notes[0].text == "sample note"
