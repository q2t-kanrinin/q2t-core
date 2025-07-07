from src.models.eval_axis import EvalAxis


def test_eval_axis_str():
    axis = EvalAxis(
        structure_depth=3,
        link_density=0.4,
        semantic_tension=0.2,
        template_type="basic",
        valid=False,
    )
    text = str(axis)
    assert "structure_depth=3" in text
    assert "link_density=0.4" in text
    assert "semantic_tension=0.2" in text
    assert "template_type='basic'" in text
    assert "valid=False" in text
