from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ASTNode:
    """Node in the abstract syntax tree with φψμ coordinates."""

    id: str
    label: str
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    phi: float = 0.0
    psi: float = 0.0
    mu: float = 0.0


@dataclass
class ASTEdge:
    """Edge connecting two :class:`ASTNode` objects."""

    id: str
    source: str
    target: str
    label: str
    weight: float = 1.0
    phi: float = 0.0
    psi: float = 0.0
    mu: float = 0.0


__all__ = ["ASTNode", "ASTEdge"]
