"""Data models representing the FoldDSL schema."""

from __future__ import annotations
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import List, Optional


class NoteNode(BaseModel):
    """Non-structural annotation node."""

    text: str

class Section(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    tension: int = Field(0, ge=0, le=3)
    children: List[Section] = Field(default_factory=list)
    notes: List[NoteNode] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def convert_children_and_notes(cls, values: dict):
        """Normalize children and note nodes before validation."""
        if not isinstance(values, dict):
            return values

        raw_children = values.get("children", [])
        processed_children: List[dict | "Section"] = []
        collected_notes: List[NoteNode] = []

        for child in raw_children:
            if isinstance(child, dict) and "@note" in child:
                collected_notes.append(NoteNode(text=str(child["@note"])))
            else:
                processed_children.append(child)

        if "@note" in values:
            collected_notes.append(NoteNode(text=str(values.pop("@note"))))

        # convert pre-supplied notes
        for n in values.get("notes", []):
            if isinstance(n, NoteNode):
                collected_notes.append(n)
            elif isinstance(n, dict) and "@note" in n:
                collected_notes.append(NoteNode(text=str(n["@note"])))
            else:
                collected_notes.append(NoteNode.model_validate(n))

        values["children"] = processed_children
        values["notes"] = collected_notes
        values.setdefault("tension", 0)

        return values

class Link(BaseModel):
    source: str
    target: str
    type: str
    weight: float = Field(..., ge=0.0, le=1.0)

class Meta(BaseModel):
    version: str
    created: str
    author: str
    tags: List[str] = Field(default_factory=list)

class Semantic(BaseModel):
    keywords: List[str] = Field(default_factory=list)
    themes: List[str] = Field(default_factory=list)

class FoldDSL(BaseModel):
    id: str
    title: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    sections: List[Section] = Field(alias="section")
    links: List[Link]
    meta: Meta
    semantic: Semantic

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values):
        if "id" not in values:
            raise ValueError("Field 'id' is required.")
        return values

    @model_validator(mode="after")
    def validate_structure(self) -> "FoldDSL":
        ids: List[str] = []
        for root in self.sections:
            ids.extend(_collect_ids(root))

        if len(ids) != len(set(ids)):
            raise ValueError("section.id must be unique")

        for link in self.links:
            if link.source not in ids:
                raise ValueError(f"link source '{link.source}' is not defined in sections")
            if link.target not in ids:
                raise ValueError(f"link target '{link.target}' is not defined in sections")

        return self

def _collect_ids(section: Section) -> List[str]:
    ids = [section.id]
    for child in section.children:
        ids.extend(_collect_ids(child))
    return ids

__all__ = ["Section", "Link", "Meta", "Semantic", "FoldDSL", "NoteNode"]
