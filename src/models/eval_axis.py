"""Data class describing evaluation axis metrics for Zettel templates."""

from dataclasses import dataclass


@dataclass
class EvalAxis:
    """Evaluation axis for Zettel templates."""

    structure_depth: int
    link_density: float
    semantic_tension: float
    template_type: str
    valid: bool = True

    def __str__(self) -> str:
        return (
            "EvalAxis("
            f"structure_depth={self.structure_depth}, "
            f"link_density={self.link_density}, "
            f"semantic_tension={self.semantic_tension}, "
            f"template_type='{self.template_type}', "
            f"valid={self.valid})"
        )


__all__ = ["EvalAxis"]
