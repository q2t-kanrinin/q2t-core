import yaml
from pathlib import Path

from src.utils.eval_utils import load_eval_config


def test_load_eval_config(tmp_path: Path) -> None:
    cfg = {
        "title": "example",
        "axes": [
            {"axis": "A", "items": []}
        ],
    }
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")

    data = load_eval_config(str(path))

    assert data["title"] == "example"
    assert data["axes"][0]["axis"] == "A"

