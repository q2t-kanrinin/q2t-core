from src.utils.dsl_parser import DSLParser
from src.utils.graphviz_generator import generate_graphviz_from_fold_dsl


def test_graphviz_contains_tooltips():
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()

    graph = generate_graphviz_from_fold_dsl(dsl)
    source = graph.source

    assert "tooltip" in source
    for kw in dsl.semantic.keywords:
        assert kw in source
    for theme in dsl.semantic.themes:
        assert theme in source
