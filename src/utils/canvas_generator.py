"""Generate Obsidian Canvas data from :class:`FoldDSL`."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Sequence

from src.models.fold_dsl import FoldDSL, Section, Link
from .dsl_parser import DSLParser

TENSION_COLOR_MAP: Dict[int, str] = {
    0: "#cccccc",
    1: "#3399ff",
    2: "#ffaa33",
    3: "#ff3333",
}


def _collect_linked_nodes(links: Sequence[Link]) -> set[str]:
    """Gather node identifiers referenced by *links*.

    Parameters
    ----------
    links : Sequence[Link]
        Link objects from which to collect ``source`` and ``target`` IDs.

    Returns
    -------
    set[str]
        Unique node IDs appearing in the link list.
    """

    nodes: set[str] = set()
    for l in links:
        nodes.add(l.source)
        nodes.add(l.target)
    return nodes


def _state_marker(section: Section, dsl: FoldDSL, linked: set[str]) -> List[str]:
    """Return state marker labels for a section on the canvas.

    Parameters
    ----------
    section : Section
        Section to evaluate.
    dsl : FoldDSL
        FoldDSL instance containing semantic information.
    linked : set[str]
        Node IDs that participate in links.

    Returns
    -------
    List[str]
        Marker tokens ``phi``, ``psi`` and/or ``mu``.
    """

    marks: List[str] = []
    if dsl.semantic and dsl.semantic.keywords:
        marks.append("phi")
    if dsl.semantic and dsl.semantic.themes:
        marks.append("psi")
    if (section.tension or 0) > 0 or section.id in linked:
        marks.append("mu")
    return marks


def generate_canvas_from_fold_dsl(src: FoldDSL | str | Path) -> Dict[str, Any]:
    """Convert a :class:`FoldDSL` instance to Obsidian Canvas JSON structure."""

    if isinstance(src, (str, Path)):
        parser = DSLParser(str(src))
        dsl = parser.parse()
    else:
        dsl = src

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    linked_nodes = _collect_linked_nodes(dsl.links)

    def traverse(section: Section) -> None:
        pos = getattr(section, "position", {}) or {}
        phi = pos.get("phi", 0)
        psi = pos.get("psi", 0)
        mu_val = pos.get("mu")

        node: Dict[str, Any] = {
            "id": section.id,
            "label": section.name,
            "type": "text",
            "x": phi * 300,
            "y": psi * 300,
            "color": TENSION_COLOR_MAP.get(section.tension, "#cccccc"),
            "state_marker": _state_marker(section, dsl, linked_nodes),
        }

        metadata = {"tension": section.tension}
        if mu_val is not None:
            metadata["mu"] = mu_val
        if dsl.semantic and dsl.semantic.keywords:
            metadata["keywords"] = dsl.semantic.keywords
        if dsl.semantic and dsl.semantic.themes:
            metadata["themes"] = dsl.semantic.themes

        if metadata:
            node["metadata"] = metadata

        nodes.append(node)

        for child in section.children:
            traverse(child)

    for root in dsl.sections:
        traverse(root)

    for link in dsl.links:
        edge = {
            "id": f"edge-{link.source}-{link.target}",
            "source": link.source,
            "target": link.target,
            "type": link.type,
            "weight": link.weight,
        }
        edges.append(edge)

    return {"nodes": nodes, "edges": edges}


__all__ = ["generate_canvas_from_fold_dsl"]
