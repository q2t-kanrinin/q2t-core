import json
from pathlib import Path
from src.utils.dsl_parser import DSLParser
from src.utils.canvas_generator import generate_canvas


def test_generate_canvas_minimal(tmp_path):
    yaml_text = """
    #title: Test Fold
    #tags: [test]
    section:
      id: root
      name: Root Node
      tension: 2
      children:
        - id: child
          name: Child Node
          tension: 1
    links:
      - source: root
        target: child
        type: bridge
    meta:
      version: "0.1"
      created: "2025-07-09"
      author: tester
    semantic:
      keywords: []
      themes: []
    """
    fold_path = tmp_path / "test_fold.yaml"
    fold_path.write_text(yaml_text, encoding="utf-8")

    fold = DSLParser(str(fold_path)).parse()
    canvas = generate_canvas(fold)

    assert "nodes" in canvas
    assert "edges" in canvas
    assert len(canvas["nodes"]) == 2
    assert len(canvas["edges"]) == 1

    node_ids = [n["id"] for n in canvas["nodes"]]
    assert "root" in node_ids
    assert "child" in node_ids

    edge = canvas["edges"][0]
    assert edge["source"] == "root"
    assert edge["target"] == "child"
    assert edge["type"] == "bridge"

    # オプション：Canvas構造を一時ファイルに保存して中身を確認
    output_path = tmp_path / "out.canvas"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(canvas, f, indent=2, ensure_ascii=False)

    assert output_path.exists()
