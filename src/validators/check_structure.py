"""Validators for FoldDSL link structures and text checks."""

from __future__ import annotations

from typing import List, Set

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
    seen: Set[tuple[str, str, str]] = set()
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

        link_key = (link["source"], link["target"], link["type"])
        if link_key in seen:
            line = link.lc.line + 1 if hasattr(link, "lc") else "unknown"
            raise ValueError(f"Duplicate link detected at line {line}")
        seen.add(link_key)


ALLOWED_COMMANDS = {
    "節点",
    "接続",
    "属性",
    "意味",
    "状態",
    "型",
    "分岐",
    "注釈",
    "変化",
    "ラベル",
    "未定",
}


def check_fold_dsl(path: str) -> None:
    """Run static checks on a fold_dsl text file.

    Prints warnings on undefined commands, invalid indentation hierarchy and
    duplicate node IDs.
    """

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    indent_stack: List[int] = []
    prev_indent = 0
    last_command: str | None = None
    node_ids: Set[str] = set()

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        parts = stripped.split()
        command = parts[0]

        if command not in ALLOWED_COMMANDS:
            print(f"{path}:{lineno}: 未定義の命令語 '{command}'")

        if command == "節点":
            node_id = parts[1] if len(parts) > 1 else ""
            if node_id:
                if node_id in node_ids:
                    print(f"{path}:{lineno}: 同一ノードID '{node_id}' が重複")
                else:
                    node_ids.add(node_id)

            if indent > prev_indent and last_command != "節点":
                print(f"{path}:{lineno}: 階層インデントが不正")

            while indent_stack and indent <= indent_stack[-1]:
                indent_stack.pop()
            indent_stack.append(indent)
            last_command = "節点"
            prev_indent = indent
            continue

        if indent > prev_indent:
            print(f"{path}:{lineno}: 階層インデントが不正")

        prev_indent = indent
        last_command = command

__all__ = ["validate_links", "check_fold_dsl"]
