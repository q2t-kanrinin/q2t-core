from __future__ import annotations

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.models.fold_dsl import FoldDSL


def validate_links(dsl: FoldDSL, yaml_path: str) -> None:
    """Validate link structures in the YAML file.

    Parameters
    ----------
    dsl : FoldDSL
        Parsed FoldDSL instance whose links will be validated.
    yaml_path : str
        Path to the original YAML file. Used to obtain line numbers for
        error reporting.
    """
    yaml = YAML()
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.load(f)

    links = data.get("links", [])
    for idx, link in enumerate(links):
        if not isinstance(link, CommentedMap):
            line = getattr(link, "lc", None)
            line_num = line.line + 1 if line else "unknown"
            raise ValueError(f"Invalid link entry type at line {line_num}")

        required_keys = ["source", "target", "type", "weight"]
        for key in required_keys:
            if key not in link:
                line = link.lc.line + 1 if hasattr(link, "lc") else "unknown"
                raise ValueError(f"Missing '{key}' in link at line {line}")

        # type checks
        if not isinstance(link["source"], str):
            line = link.lc.value("source")[0] + 1
            raise ValueError(f"'source' must be str at line {line}")
        if not isinstance(link["target"], str):
            line = link.lc.value("target")[0] + 1
            raise ValueError(f"'target' must be str at line {line}")
        if not isinstance(link["type"], str):
            line = link.lc.value("type")[0] + 1
            raise ValueError(f"'type' must be str at line {line}")

        weight = link["weight"]
        if not isinstance(weight, (float, int)):
            line = link.lc.value("weight")[0] + 1
            raise ValueError(f"'weight' must be float at line {line}")
        if not 0.0 <= float(weight) <= 1.0:
            line = link.lc.value("weight")[0] + 1
            raise ValueError(f"'weight' out of range at line {line}")

__all__ = ["validate_links"]
