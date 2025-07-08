import json
from pathlib import Path

from utils.dsl_parser import DSLParser
from utils.canvas_generator import generate_canvas_from_fold_dsl


def test_generate_canvas_from_sample_yaml():
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()

    canvas = generate_canvas_from_fold_dsl(dsl)

    assert "nodes" in canvas
    assert "edges" in canvas
    assert isinstance(canvas["nodes"], list)
    assert isinstance(canvas["edges"], list)
    assert len(canvas["nodes"]) > 0

    allowed_colors = {"#cccccc", "#3399ff", "#ffaa33", "#ff3333"}
    for node in canvas["nodes"]:
        assert {"id", "label", "x", "y", "color"}.issubset(node)
        assert node["color"] in allowed_colors
        assert "state_marker" in node
        assert isinstance(node["state_marker"], list)
        for mark in node["state_marker"]:
            assert mark in ["phi", "psi", "mu"]

    for edge in canvas["edges"]:
        assert {"id", "source", "target", "type", "weight"}.issubset(edge)


def test_canvas_output_to_file(tmp_path: Path):
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()
    canvas = generate_canvas_from_fold_dsl(dsl)

    out_path = tmp_path / "fold_canvas.canvas"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(canvas, f, ensure_ascii=False, indent=2)

    assert out_path.exists()
    content = json.loads(out_path.read_text(encoding="utf-8"))
    assert "nodes" in content and "edges" in content
