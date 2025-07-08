"""Analyze tension logs and adjust :class:`FoldDSL` instances."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from src.models.fold_dsl import FoldDSL, Section


class TensionAnalyzer:
    """Analyze logged tension history and update structures accordingly."""

    def __init__(self, log_dir: str | Path = "log") -> None:
        self.log_dir = Path(log_dir)

    def _load_logs(self) -> List[Dict[str, int]]:
        logs: List[Dict[str, int]] = []
        if not self.log_dir.exists():
            return logs
        for file in sorted(self.log_dir.glob("tension_*.json")):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                tensions = data.get("tensions", {})
                if isinstance(tensions, dict):
                    logs.append({k: int(v) for k, v in tensions.items()})
            except Exception:
                continue
        return logs

    def _average_tension(self) -> Dict[str, float]:
        logs = self._load_logs()
        totals: Dict[str, List[int]] = defaultdict(list)
        for entry in logs:
            for sec_id, value in entry.items():
                totals[sec_id].append(value)
        return {k: sum(v) / len(v) for k, v in totals.items() if v}

    def adjust_fold_dsl(self, dsl: FoldDSL) -> None:
        """Update tensions of *dsl* sections based on log averages."""
        averages = self._average_tension()

        def apply(section: Section) -> None:
            avg = averages.get(section.id)
            if avg is not None:
                section.tension = max(0, min(3, int(round(avg))))
            for child in section.children:
                apply(child)

        for root in dsl.sections:
            apply(root)


__all__ = ["TensionAnalyzer"]
