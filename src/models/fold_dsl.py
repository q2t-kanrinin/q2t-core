from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, root_validator


class Section(BaseModel):
    """Represents a fold section node."""

    id: str
    name: str
    description: Optional[str] = None
    tension: int = Field(0, ge=0, le=3)
    children: List["Section"] = Field(default_factory=list)


class Link(BaseModel):
    """Represents a bridge link between sections."""

    source: str
    target: str
    type: str
    weight: float = Field(..., ge=0.0, le=1.0)


class Meta(BaseModel):
    """Metadata for a fold DSL document."""

    version: str
    created: str
    author: str
    tags: List[str] = Field(default_factory=list)


class Semantic(BaseModel):
    """Optional semantic information."""

    keywords: List[str] = Field(default_factory=list)
    themes: List[str] = Field(default_factory=list)


class FoldDSL(BaseModel):
    """Root model for a fold DSL document."""

    section: Section
    links: List[Link] = Field(default_factory=list)
    meta: Meta
    semantic: Optional[Semantic] = None

    @root_validator
    def _validate_integrity(cls, values: dict) -> dict:
        section = values.get("section")
        if section is None:
            raise ValueError("section is required")

        ids = list(_collect_ids(section))
        if len(ids) != len(set(ids)):
            raise ValueError("section.id must be unique")

        link_list: List[Link] = values.get("links", [])
        for link in link_list:
            if link.source not in ids:
                raise ValueError(
                    f"link source '{link.source}' is not defined in sections"
                )
            if link.target not in ids:
                raise ValueError(
                    f"link target '{link.target}' is not defined in sections"
                )
        return values


def _collect_ids(section: Section) -> List[str]:
    """Recursively collect IDs from a section tree."""

    ids = [section.id]
    for child in section.children:
        ids.extend(_collect_ids(child))
    return ids


__all__ = ["Section", "Link", "Meta", "Semantic", "FoldDSL"]
