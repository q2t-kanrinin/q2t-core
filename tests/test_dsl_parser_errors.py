import textwrap
from pathlib import Path
import pytest

from src.utils.dsl_parser import DSLParser
from src.models.fold_dsl import FoldDSL, Section, Meta, Semantic
from src.validators.check_structure import validate_links


def _write_yaml(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "sample.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_parse_missing_section(tmp_path: Path) -> None:
    yaml_text = textwrap.dedent(
        """\
        links: []
        meta:
          version: "0.1"
          created: "2025-07-07"
          author: tester
        semantic:
          keywords: []
          themes: []
        """
    )
    path = _write_yaml(tmp_path, yaml_text)
    parser = DSLParser(str(path))
    with pytest.raises(ValueError):
        parser.parse()


def test_validate_links_weight_out_of_range(tmp_path: Path) -> None:
    yaml_text = textwrap.dedent(
        """\
        section:
          id: root
          name: Root
        links:
          - source: A
            target: B
            type: rel
            weight: 1.5
        meta:
          version: "0.1"
          created: "2025-01-01"
          author: tester
        semantic:
          keywords: []
          themes: []
        """
    )
    path = _write_yaml(tmp_path, yaml_text)
    dsl = FoldDSL(
        id="x",
        sections=[Section(id="root", name="root")],
        links=[],
        meta=Meta(version="0.1", created="2025-01-01", author="tester"),
        semantic=Semantic(),
    )

    with pytest.raises(ValueError):
        validate_links(dsl, str(path))


def test_validate_links_missing_target(tmp_path: Path) -> None:
    yaml_text = textwrap.dedent(
        """\
        section:
          id: root
          name: Root
        links:
          - source: A
            type: rel
            weight: 0.5
        meta:
          version: "0.1"
          created: "2025-01-01"
          author: tester
        semantic:
          keywords: []
          themes: []
        """
    )
    path = _write_yaml(tmp_path, yaml_text)
    dsl = FoldDSL(
        id="x",
        sections=[Section(id="root", name="root")],
        links=[],
        meta=Meta(version="0.1", created="2025-01-01", author="tester"),
        semantic=Semantic(),
    )

    with pytest.raises(ValueError):
        validate_links(dsl, str(path))
