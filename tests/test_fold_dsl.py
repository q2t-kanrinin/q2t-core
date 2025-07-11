from src.models.fold_dsl import FoldDSL, Section, Link, Meta, Semantic
import pytest

def test_fold_dsl_valid():
    section = Section(
        id="A-01",
        name="境界",
        description="環境構造に関するトポ界隈",
        tension=2,
        children=[
            Section(
                id="A-01-01",
                name="構文",
                children=[
                    Section(id="A-01-01-01", name="共起性"),
                    Section(id="A-01-01-02", name="差異原理"),
                ]
            ),
            Section(id="A-01-02", name="言語階層"),
        ]
    )

    links = [
        Link(source="A-01-01-01", target="A-01-02", type="related", weight=0.7),
        Link(source="A-01-01-02", target="A-01", type="context", weight=0.5),
    ]

    meta = Meta(version="0.1", created="2025-07-07", author="q2t-kanrinin", tags=["構造"])
    semantic = Semantic(keywords=["境界", "構文", "言語階層"], themes=["ψψモデル"])

    dsl = FoldDSL(
        id="test-001",  # ✅ 明示必須
        sections=[section],
        links=links,
        meta=meta,
        semantic=semantic,
        tags=["unit"]
    )

    assert dsl.id == "test-001"
    assert len(dsl.sections) == 1
    assert dsl.meta.author == "q2t-kanrinin"
    assert dsl.tags == ["unit"]


def test_fold_dsl_duplicate_section_id():
    section = Section(id="A-01", name="root", children=[Section(id="A-01", name="dup")])
    meta = Meta(version="0.1", created="2025-07-07", author="tester")
    semantic = Semantic()

    with pytest.raises(ValueError, match="section.id must be unique"):
        FoldDSL(id="dup-test", sections=[section], links=[], meta=meta, semantic=semantic)


def test_fold_dsl_link_invalid_target():
    section = Section(id="A-01", name="root")
    meta = Meta(version="0.1", created="2025-07-07", author="tester")
    semantic = Semantic()
    links = [Link(source="A-01", target="nonexistent", type="related", weight=0.5)]

    with pytest.raises(ValueError, match="link target 'nonexistent' is not defined"):
        FoldDSL(id="link-test", sections=[section], links=links, meta=meta, semantic=semantic)
