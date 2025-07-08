"""Generate Graphviz representation from :class:`FoldDSL`."""

from __future__ import annotations

from pathlib import Path

from graphviz import Digraph

from src.models.fold_dsl import FoldDSL, Section, Link
from .dsl_parser import DSLParser


def generate_graphviz_from_fold_dsl(src: FoldDSL | str | Path) -> Digraph:
    """Create a Graphviz ``Digraph`` from a :class:`FoldDSL` instance.

    Parameters
    ----------
    src : FoldDSL | str | Path
        Parsed FoldDSL object or path to a YAML file.
    """
    if isinstance(src, (str, Path)):
        parser = DSLParser(str(src))
        dsl = parser.parse()
    else:
        dsl = src

    dot = Digraph("FoldDSL")

    tooltip_lines: list[str] = []
    if dsl.semantic.keywords:
        tooltip_lines.append("keywords: " + ", ".join(dsl.semantic.keywords))
    if dsl.semantic.themes:
        tooltip_lines.append("themes: " + ", ".join(dsl.semantic.themes))
    tooltip = "\n".join(tooltip_lines) if tooltip_lines else None

    def add_section(section: Section) -> None:
        label = f"{section.name} ({section.id})"
        dot.node(section.id, label=label, tooltip=tooltip)
        for child in section.children:
            add_section(child)
            dot.edge(section.id, child.id, label="child")

    for root in dsl.sections:
        add_section(root)

    for link in dsl.links:
        dot.edge(link.source, link.target, label=link.type)

    return dot


__all__ = ["generate_graphviz_from_fold_dsl"]
