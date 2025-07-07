from typing import Dict, Any
from src.models.fold_dsl import FoldDSL, Section


def generate_canvas(fold: FoldDSL) -> Dict[str, Any]:
    nodes = []
    edges = []

    def resolve_position(section: Section) -> Dict[str, int]:
        pos = getattr(section, "position", {}) or {}
        x = 300 * pos.get("phi", 0)
        y = 300 * pos.get("psi", 0)
        return {"x": x, "y": y}

    def resolve_color(tension: int) -> str:
        return {
            0: "#cccccc",
            1: "#3399ff",
            2: "#ffaa33",
            3: "#ff3333"
        }.get(tension, "#cccccc")

    def add_nodes(section: Section):
        position = resolve_position(section)
        tension = section.tension or 0
        label = section.name

        if getattr(fold, "state_marker", []):
            markers = ", ".join(fold.state_marker)
            label += f" [{markers}]"

        nodes.append({
            "id": section.id,
            "type": "text",
            "label": label,
            "position": position,
            "color": resolve_color(tension)
        })
        for child in section.children:
            add_nodes(child)

    for section in fold.sections:
        add_nodes(section)

    for link in fold.links:
        edges.append({
            "id": f"edge-{link.source}-{link.target}",
            "source": link.source,
            "target": link.target,
            "type": link.type
        })

    return {"nodes": nodes, "edges": edges}


def save_canvas(canvas: dict, path: str) -> None:
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(canvas, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    from src.utils.dsl_parser import DSLParser
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    fold = parser.parse()
    canvas = generate_canvas(fold)
    save_canvas(canvas, "docs/fold_canvas.canvas")
