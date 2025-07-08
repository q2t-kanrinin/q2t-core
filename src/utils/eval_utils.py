import yaml
from typing import Any, Dict


def load_eval_config(path: str) -> Dict[str, Any]:
    """Load evaluation configuration from a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
