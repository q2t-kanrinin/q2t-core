import tempfile
from pathlib import Path

from src.models.fold_dsl import FoldDSL
from parse_fold_dsl import parse_fold_dsl


def test_parse_fold_dsl_with_comments(tmp_path: Path) -> None:
    yaml_content = """\
# sample FoldDSL with comments
id: test-001
sections: # comment for sections
  - id: A-01
    name: SectionA
links: []
meta:
  version: "0.1"
  created: "2025-07-07"
  author: "tester"
semantic:
  keywords: []
  themes: []
"""
    file_path = tmp_path / "sample.yaml"
    file_path.write_text(yaml_content, encoding="utf-8")

    dsl, comments = parse_fold_dsl(str(file_path))

    assert isinstance(dsl, FoldDSL)
    assert dsl.id == "test-001"
    assert comments.get("sections") == "comment for sections"

