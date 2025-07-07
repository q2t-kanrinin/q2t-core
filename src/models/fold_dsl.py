def test_fold_dsl_valid():
    """正常系: fold_dsl-sample.yaml相当の構造"""

    section = Section(
        id="A-01",
        name="課題",
        description="環境構造に関するトップ階層",
        tension=2,
        children=[
            Section(
                id="A-01-01",
                name="構文",
                children=[
                    Section(id="A-01-01-01", name="共起性"),
                    Section(id="A-01-01-02", name="変形限定"),
                ],
            ),
            Section(id="A-01-02", name="言語習得"),
        ],
    )

    links = [
        Link(source="A-01-01", target="A-01-02", type="related", weight=0.7),
        Link(source="A-01-01-02", target="A-01", type="context", weight=0.5),
    ]

    meta = Meta(version="0.1", created="2025-07-07", author="q2t-kanrinin", tags=["構造"])
    semantic = Semantic(keywords=["課題", "構文", "言語習得"], themes=["qψψモデル"])

    dsl = FoldDSL(
        id="test-001",  # ← 必須項目を明示
        sections=[section],  # ← List[Section]
        links=links,
        meta=meta,
        semantic=semantic,
    )

    assert dsl.id == "test-001"
    assert len(dsl.sections) == 1
    assert dsl.meta.author == "q2t-kanrinin"
