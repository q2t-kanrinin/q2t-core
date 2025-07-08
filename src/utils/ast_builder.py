from __future__ import annotations

from typing import Dict, List, Tuple

from src.models.fold_dsl import FoldDSL, Section, Link
from src.models.ast import ASTNode, ASTEdge


class ASTBuilder:
    """Build an AST representation from :class:`FoldDSL`."""

    @staticmethod
    def parse_dsl(dsl: FoldDSL) -> Tuple[List[ASTNode], List[ASTEdge]]:
        """Convert a :class:`FoldDSL` to lists of nodes and edges."""

        nodes_map: Dict[str, ASTNode] = {}
        edges: List[ASTEdge] = []

        def _traverse(section: Section, parent: str | None = None) -> None:
            pos = getattr(section, "position", {}) or {}
            phi = float(pos.get("phi", 0))
            psi = float(pos.get("psi", 0))
            mu = float(pos.get("mu", 0))

            node = ASTNode(
                id=section.id,
                label=section.name,
                parent=parent,
                phi=phi,
                psi=psi,
                mu=mu,
            )
            nodes_map[section.id] = node
            if parent:
                nodes_map[parent].children.append(section.id)
            for child in section.children:
                _traverse(child, section.id)

        for root in dsl.sections:
            _traverse(root)

        for idx, link in enumerate(dsl.links):
            edge = ASTEdge(
                id=f"edge-{idx}",
                source=link.source,
                target=link.target,
                label=link.type,
                weight=link.weight,
            )
            edges.append(edge)

        return list(nodes_map.values()), edges


__all__ = ["ASTBuilder"]
