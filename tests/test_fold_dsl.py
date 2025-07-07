import pytest
from src.models.fold_dsl import FoldDSL, Section, Link, Meta, Semantic


def test_fold_dsl_valid():
    """正常系: fold_dsl-sample.yaml相当の構造"""
    section = Section(
        id="A-01",
        name="抽象",
        description="抽象概念に関するトップ階層",
        tension=2,
        children=[
            Section(
                id="A-01-01",
                name="概念",
                children=[
                    Section(id="A-01-01-01", name="共通性"),
                    Section(id="A-01-01-02", name="差異性"),
                ],
            ),
            Section(id="A-01-02", name="普遍"),
        ],
    )

    links = [
        Link(source="A-01-01-01", target="A-01-02", type="related", weight=0.7),
        Link(source="A-01-01-02", target="A-01", type="context", weight=0.5),
    ]

    meta = Meta(version="0.1", created="2025-07-07", author="q2t-kanrinin", tags=["抽象"])
    semantic = Semantic(keywords=["抽象", "概念"], themes=["φψμモデル"])

    dsl = FoldDSL(section=section, links=links, meta=meta, semantic=semantic)
    assert dsl.section.id == "A-01"
    assert len(dsl.links) == 2


def test_fold_dsl_duplicate_section_id():
    """異常系: section.idが重複"""
    section = Section(
        id="A-01",
        name="抽象",
        children=[
            Section(id="A-01", name="重複ID"),
        ],
    )
    meta = Meta(version="0.1", created="2025-07-07", author="q2t")
    with pytest.raises(ValueError, match="section.id must be unique"):
        FoldDSL(section=section, meta=meta)


def test_fold_dsl_link_invalid_target():
    """異常系: linksのtargetが存在しない"""
    section = Section(id="A-01", name="抽象")
    meta = Meta(version="0.1", created="2025-07-07", author="q2t")
    links = [
        Link(source="A-01", target="nonexistent", type="related", weight=0.5)
    ]
    with pytest.raises(ValueError, match="link target 'nonexistent' is not defined"):
        FoldDSL(section=section, meta=meta, links=links)
