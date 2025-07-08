from pathlib import Path
import json

from src.utils.dsl_parser import DSLParser
from src.utils.tension_tracker import TensionTracker


def create_sample_yaml(path: Path, tension_root: int = 1, tension_child: int = 0) -> None:
    yaml_text = f"""
section:
  id: root
  name: Root
  tension: {tension_root}
  children:
    - id: child
      name: Child
      tension: {tension_child}
links: []
meta:
  version: "0.1"
  created: "2025-01-01"
  author: tester
semantic:
  keywords: []
  themes: []
"""
    path.write_text(yaml_text, encoding="utf-8")


def test_tension_tracker_records(tmp_path: Path) -> None:
    yaml_path = tmp_path / "sample.yaml"
    create_sample_yaml(yaml_path, 1, 0)

    parser = DSLParser(str(yaml_path))
    dsl = parser.parse()

    tracker = TensionTracker(log_dir=tmp_path)
    first_log = tracker.record(dsl)

    assert len(tracker.history) == 1
    assert tracker.history[0]["root"] == 1
    assert tracker.history[0]["child"] == 0
    assert first_log.exists()

    data = json.loads(first_log.read_text(encoding="utf-8"))
    assert data["tensions"]["root"] == 1

    # update tension and record again
    dsl.sections[0].tension = 2
    second_log = tracker.record(dsl)

    assert len(tracker.history) == 2
    assert tracker.history[1]["root"] == 2
    assert second_log.exists()

    logs = list(tmp_path.glob("tension_*.json"))
    assert len(logs) == 2
