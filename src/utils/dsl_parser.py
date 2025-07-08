"""Utility for parsing FoldDSL YAML files with comment metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
import re

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.models.fold_dsl import FoldDSL, Section, NoteNode


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

        if "\u2705" in raw:
            raw = raw.split("\u2705", 1)[0]

        # allow unquoted `@note` keys
        raw = re.sub(r'(^\s*-?\s*)@note:', r'\1"@note":', raw, flags=re.MULTILINE)

        data: CommentedMap = self.yaml.load(raw)

        meta_from_comments = self._extract_comment_metadata(data)
        self.meta_tags = meta_from_comments.get("tags", [])

if "section" in data:
    data["sections"] = [data.pop("section")]

raw_sections = data.get("sections", [])
sections = [self._parse_section(s) for s in raw_sections]
data["sections"] = sections

for link in data.get("links", []):
    if "weight" not in link:
        link["weight"] = 1.0

if "id" not in data and sections:
    data["id"] = sections[0].id

dsl = FoldDSL.model_validate(data)
dsl.title = meta_from_comments.get("title")
dsl.tags = meta_from_comments.get("tags", [])
return dsl

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
        raw_children = data.get("children", [])
        children: List[Section] = []
        notes: List[NoteNode] = []

        for child in raw_children:
            if isinstance(child, dict) and "@note" in child:
                notes.append(NoteNode(text=str(child["@note"])))
            else:
                children.append(self._parse_section(child))

        if "@note" in data:
            notes.append(NoteNode(text=str(data["@note"])))

        return Section(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            tension=data.get("tension", 0),
            children=children,
            notes=notes,
        )

__all__ = ["DSLParser"]
