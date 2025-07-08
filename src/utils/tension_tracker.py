"""Utility for logging section tension values over time."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from src.models.fold_dsl import FoldDSL, Section


class TensionTracker:
    """Record tension snapshots for a :class:`FoldDSL` instance."""

    def __init__(self, log_dir: str | Path = "log") -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history: list[Dict[str, int]] = []

    def _collect(self, section: Section) -> Dict[str, int]:
        tensions = {section.id: section.tension}
        for child in section.children:
            tensions.update(self._collect(child))
        return tensions

    def record(self, dsl: FoldDSL) -> Path:
        """Append current tensions to history and write a log file."""
        tensions: Dict[str, int] = {}
        for root in dsl.sections:
            tensions.update(self._collect(root))

        self.history.append(tensions)

        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%d-%H%M%S-%f")
        path = self.log_dir / f"tension_{timestamp}.json"
        data = {"timestamp": now.isoformat(), "tensions": tensions}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path


__all__ = ["TensionTracker"]

