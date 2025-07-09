from src.utils import (
    DSLParser,
    generate_graphviz_from_fold_dsl,
    generate_canvas_from_fold_dsl,
    compute_eval_scores,
    validate_links,
    export_dataview_markdown,
    TensionTracker,
    TensionAnalyzer,
)


def test_utils_init_exports():
    assert callable(DSLParser)
    assert callable(generate_graphviz_from_fold_dsl)
    assert callable(generate_canvas_from_fold_dsl)
    assert callable(compute_eval_scores)
    assert callable(validate_links)
    assert callable(export_dataview_markdown)
    assert callable(TensionTracker)
    assert callable(TensionAnalyzer)
