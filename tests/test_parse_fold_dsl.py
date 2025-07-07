import textwrap

from parse_fold_dsl import parse_fold_dsl
from src.models.fold_dsl import FoldDSL


def test_parse_fold_dsl_with_comments(tmp_path):
    yaml_content = textwrap.dedent(
        """
        #title: Example Fold
        #tags: [demo, test]
        id: ex-001
        sections:
          - id: S-1
            name: Root
        links: []
        meta:
          version: "0.1"
          created: "2025-07-09"
          author: tester
        semantic:
          keywords: [Root]
          themes: []
        """
    )
    path = tmp_path / "sample.yaml"
    path.write_text(yaml_content, encoding="utf-8")

    dsl = parse_fold_dsl(str(path))
    assert isinstance(dsl, FoldDSL)
    assert dsl.title == "Example Fold"
    assert dsl.meta.tags == ["demo", "test"]
    assert dsl.sections[0].id == "S-1"
    assert dsl.meta.author == "tester"
