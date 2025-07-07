import uuid
from typing import Dict, Any, List

from src.models.fold_dsl import FoldDSL, Section, Link


def generate_canvas_from_fold_dsl(dsl: FoldDSL) -> Dict[str, Any]:
    nodes = []
    edges = []

    # どのノードがbridge対象かを事前に収集
    bridge_nodes = set()
    for link in dsl.links:
        bridge_nodes.add(link.source)
        bridge_nodes.add(link.target)

    def get_state_marker(section: Section) -> List[str]:
        stages = []
        if dsl.semantic and dsl.semantic.keywords:
            stages.append("phi")
        if dsl.semantic and dsl.semantic.themes:
            stages.append("psi")
        if (section.tension or 0) > 0 or section.id in bridge_nodes:
            stages.append("mu")
        return stages

    def traverse(section: Section, depth: int = 0, index: int = 0, parent_id: str | None = None):
        node_id = section.id
        label = section.name

        # φψμ座標の初期推定
        phi = depth
        psi = len(section.children)
        mu = section.tension or 0

        # ノード作成
        node = {
            "id": node_id,
            "type": "text",
            "label": label,
            "position": {"phi": phi, "psi": psi, "mu": mu},
            "size": {"width": 200, "height": 100},
            "state_marker": get_state_marker(section),
            "metadata": {
                "tension": section.tension,
                "keywords": dsl.semantic.keywords,
                "themes": dsl.semantic.themes,
            },
            "content": label,
        }
        nodes.append(node)

        # 再帰的に子を処理
        for i, child in enumerate(section.children):
            traverse(child, depth + 1, i, node_id)

    # 最上位セクションのみ対象
    for root in dsl.sections:
        traverse(root)

    for link in dsl.links:
        edge = {
            "id": str(uuid.uuid4()),
            "source": link.source,
            "target": link.target,
            "type": link.type,
            "weight": link.weight,
        }
        edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges
    }
