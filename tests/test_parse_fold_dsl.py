import textwrap
from pathlib import Path

from src.models.fold_dsl import FoldDSL
from parse_fold_dsl import DSLParser


def test_dslparser_parses_zettel_metadata(tmp_path: Path) -> None:
    yaml_content = textwrap.dedent(
        """\
        #title: Example Fold
        #tags: [demo, test]
        id: ex-001
        section:
          id: S-1
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
    file_path = tmp_path / "sample.yaml"
    file_path.write_text(yaml_content, encoding="utf-8")

    parser = DSLParser(str(file_path))
    dsl = parser.parse()

    assert isinstance(dsl, FoldDSL)
    assert dsl.id == "ex-001"
    assert dsl.title == "Example Fold"
    assert parser.meta_tags == ["demo", "test"]
    assert dsl.sections[0].id == "S-1"
    assert dsl.meta.author == "tester"
    assert dsl.meta.version == "0.1"
