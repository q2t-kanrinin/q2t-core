"""Utility for parsing FoldDSL YAML files with comment metadata."""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.models.fold_dsl import FoldDSL, Section, Link, Meta, Semantic


class DSLParser:
    """Parse fold_dsl YAML files while capturing metadata from comments."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.yaml = YAML()
        self.path: Path | None = Path(path) if path is not None else None
        self.meta_tags: List[str] = []

    def parse(self, path: str | Path | None = None) -> FoldDSL:
        """Load YAML from *path* and convert to :class:`FoldDSL`."""
        target = Path(path) if path is not None else self.path
        if target is None:
            raise ValueError("path is required")
        self.path = target
        with open(target, "r", encoding="utf-8") as f:
            raw = f.read()

        if "\u2705" in raw:  # cut off non-YAML notes starting with check mark
            raw = raw.split("\u2705", 1)[0]

        data: CommentedMap = self.yaml.load(raw)

        meta_from_comments = self._extract_comment_metadata(data)
        self.meta_tags = meta_from_comments.get("tags", [])
        section = self._parse_section(data["section"])
        links = [Link(**link) for link in data.get("links", [])]
        meta = Meta(**data.get("meta", {}))
        semantic = Semantic(**data.get("semantic", {}))

        return FoldDSL(
            id=data.get("id", section.id),
            title=meta_from_comments.get("title"),
            tags=meta_from_comments.get("tags", []),
            sections=[section],
            links=links,
            meta=meta,
            semantic=semantic,
        )

    def _extract_comment_metadata(self, data: CommentedMap) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if getattr(data, "ca", None) and data.ca.comment:
            comments = data.ca.comment[1] or []
            for token in comments:
                line = token.value.strip("#").strip()
                if line.startswith("title:"):
                    result["title"] = line[len("title:"):].strip()
                elif line.startswith("tags:"):
                    tag_str = line[len("tags:"):].strip()
                    if tag_str.startswith("[") and tag_str.endswith("]"):
                        tag_str = tag_str[1:-1]
                    result["tags"] = [t.strip() for t in tag_str.split(',') if t.strip()]
        return result

    def _parse_section(self, data: Dict[str, Any]) -> Section:
        children = [self._parse_section(child) for child in data.get("children", [])]
        return Section(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            tension=data.get("tension", 0),
            children=children,
        )

__all__ = ["DSLParser"]

# 該当部分（パーサ内部）
if isinstance(item, dict) and "@note" in item:
    note_text = item["@note"]
    note = NoteNode(text=note_text)
    current_section.notes.append(note)