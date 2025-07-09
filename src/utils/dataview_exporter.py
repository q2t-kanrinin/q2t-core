"""Export FoldDSL sections as Markdown notes for Obsidian Dataview."""

from __future__ import annotations

from pathlib import Path
from typing import List, Sequence
import yaml

from src.models.fold_dsl import FoldDSL, Section, Link
from .dsl_parser import DSLParser


def _collect_linked_nodes(links: Sequence[Link]) -> set[str]:
    nodes: set[str] = set()
    for link in links:
        nodes.add(link.source)
        nodes.add(link.target)
    return nodes


def _state_marker(section: Section, dsl: FoldDSL, linked: set[str]) -> List[str]:
    marks: List[str] = []
    if dsl.semantic and dsl.semantic.keywords:
        marks.append("phi")
    if dsl.semantic and dsl.semantic.themes:
        marks.append("psi")
    if (section.tension or 0) > 0 or section.id in linked:
        marks.append("mu")
    return marks


def export_dataview_markdown(src: FoldDSL | str | Path, out_dir: str | Path) -> List[Path]:
    """Write Markdown notes with YAML frontmatter for Dataview.

    Parameters
    ----------
    src : FoldDSL | str | Path
        Parsed FoldDSL instance or path to a YAML file.
    out_dir : str | Path
        Destination directory to store generated Markdown files.
    """
    if isinstance(src, (str, Path)):
        parser = DSLParser(str(src))
        dsl = parser.parse()
    else:
        dsl = src

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    linked = _collect_linked_nodes(dsl.links)

    exported: List[Path] = []

    def traverse(sec: Section) -> None:
        frontmatter = {
            "id": sec.id,
            "title": sec.name,
            "tags": dsl.tags,
            "state_marker": _state_marker(sec, dsl, linked),
        }

        body_lines: List[str] = []
        if sec.description:
            body_lines.append(sec.description)
        for note in sec.notes:
            body_lines.append(note.text)
        body = "\n".join(body_lines) + "\n" if body_lines else ""

        yaml_text = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
        content = f"---\n{yaml_text}\n---\n\n{body}"

        file_path = out_path / f"{sec.id}.md"
        file_path.write_text(content, encoding="utf-8")
        exported.append(file_path)

        for child in sec.children:
            traverse(child)

    for root in dsl.sections:
        traverse(root)

    return exported


def main() -> None:
    """CLI entry point for exporting Markdown notes for Dataview."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Export FoldDSL sections to Markdown for Obsidian Dataview"
    )
    parser.add_argument("source", help="Path to FoldDSL YAML file")
    parser.add_argument(
        "out_dir",
        nargs="?",
        default="dataview_export",
        help="Output directory",
    )

    args = parser.parse_args()
    dsl_parser = DSLParser(args.source)
    dsl = dsl_parser.parse()
    files = export_dataview_markdown(dsl, args.out_dir)
    print(f"Exported {len(files)} files to {args.out_dir}")


__all__ = ["export_dataview_markdown", "main"]


if __name__ == "__main__":  # pragma: no cover - CLI usage
    main()
