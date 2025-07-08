from pathlib import Path
import pytest

from src.models.fold_dsl import FoldDSL, Section, Meta, Semantic
from src.validators.check_structure import validate_links


def _write_yaml(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "sample.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_validate_links_invalid_weight(tmp_path: Path):
    yaml_text = """
section:
  id: root
  name: Root
links:
  - source: A
    target: B
    type: rel
    weight: 1.2
meta:
  version: "0.1"
  created: "2025-01-01"
  author: tester
semantic:
  keywords: []
  themes: []
"""
    path = _write_yaml(tmp_path, yaml_text)
    dsl = FoldDSL(
        id="x",
        sections=[Section(id="root", name="root")],
        links=[],
        meta=Meta(version="0.1", created="2025-01-01", author="tester"),
        semantic=Semantic(),
    )

    with pytest.raises(ValueError) as exc:
        validate_links(dsl, str(path))
    assert "weight" in str(exc.value)
    assert "line" in str(exc.value)


def test_validate_links_missing_key(tmp_path: Path):
    yaml_text = """
section:
  id: root
  name: Root
links:
  - target: B
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
    path = _write_yaml(tmp_path, yaml_text)
    dsl = FoldDSL(
        id="x",
        sections=[Section(id="root", name="root")],
        links=[],
        meta=Meta(version="0.1", created="2025-01-01", author="tester"),
        semantic=Semantic(),
    )

    with pytest.raises(ValueError) as exc:
        validate_links(dsl, str(path))
    assert "source" in str(exc.value)
    assert "line" in str(exc.value)


def test_validate_links_duplicate(tmp_path: Path):
    yaml_text = """
section:
  id: root
  name: Root
links:
  - source: A
    target: B
    type: rel
    weight: 0.5
  - source: A
    target: B
    type: rel
    weight: 0.8
meta:
  version: "0.1"
  created: "2025-01-01"
  author: tester
semantic:
  keywords: []
  themes: []
"""
    path = _write_yaml(tmp_path, yaml_text)
    dsl = FoldDSL(
        id="x",
        sections=[Section(id="root", name="root")],
        links=[],
        meta=Meta(version="0.1", created="2025-01-01", author="tester"),
        semantic=Semantic(),
    )

    with pytest.raises(ValueError) as exc:
        validate_links(dsl, str(path))
    assert "duplicate" in str(exc.value).lower()
    assert "line" in str(exc.value)

