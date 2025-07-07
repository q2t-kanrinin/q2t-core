from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class Section(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    tension: int = Field(0, ge=0, le=3)
    children: List[Section] = Field(default_factory=list)

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
    sections: List[Section]
    links: List[Link]
    meta: Meta
    semantic: Semantic

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values):
        if "id" not in values:
            raise ValueError("Field 'id' is required.")
        return values

def _collect_ids(section: Section) -> List[str]:
    ids = [section.id]
    for child in section.children:
        ids.extend(_collect_ids(child))
    return ids

__all__ = ["Section", "Link", "Meta", "Semantic", "FoldDSL"]
