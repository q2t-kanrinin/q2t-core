from pathlib import Path
import yaml

from src.utils.dsl_parser import DSLParser
from src.utils.dataview_exporter import export_dataview_markdown


def test_export_dataview_markdown(tmp_path: Path) -> None:
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()

    files = export_dataview_markdown(dsl, tmp_path)

    assert files
    root_file = tmp_path / "A-01.md"
    assert root_file.exists()

    content = root_file.read_text(encoding="utf-8")
    fm_text = content.split("---", 2)[1]
    data = yaml.safe_load(fm_text)

    assert data["id"] == "A-01"
    assert "state_marker" in data

from src.models.fold_dsl import FoldDSL, Section, Link, Meta, Semantic
from src.utils.dataview_exporter import _collect_linked_nodes, _state_marker


def _simple_dsl() -> FoldDSL:
    section = Section(id="root", name="Root", tension=1, children=[Section(id="child", name="Child")])
    links = [Link(source="root", target="child", type="rel", weight=0.5)]
    meta = Meta(version="0.1", created="2025-01-01", author="tester")
    semantic = Semantic(keywords=["k"], themes=["t"])
    return FoldDSL(id="x", sections=[section], links=links, meta=meta, semantic=semantic)


def test_collect_linked_nodes() -> None:
    dsl = _simple_dsl()
    nodes = _collect_linked_nodes(dsl.links)
    assert nodes == {"root", "child"}


def test_state_marker_values() -> None:
    dsl = _simple_dsl()
    linked = _collect_linked_nodes(dsl.links)
    root_marks = _state_marker(dsl.sections[0], dsl, linked)
    assert set(root_marks) == {"phi", "psi", "mu"}

    # variant without semantic keywords/themes
    plain = FoldDSL(
        id="y",
        sections=dsl.sections,
        links=dsl.links,
        meta=dsl.meta,
        semantic=Semantic(),
    )
    linked2 = _collect_linked_nodes(plain.links)
    child_marks = _state_marker(plain.sections[0].children[0], plain, linked2)
    assert child_marks == ["mu"]

