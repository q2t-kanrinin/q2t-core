from pathlib import Path
import yaml

from src.utils.dsl_parser import DSLParser
from src.utils.dataview_exporter import export_dataview_markdown


def test_export_dataview_markdown(tmp_path: Path) -> None:
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()

    files = export_dataview_markdown(dsl, tmp_path)

    assert files
    root_file = tmp_path / "A-01.md"
    assert root_file.exists()

    content = root_file.read_text(encoding="utf-8")
    fm_text = content.split("---", 2)[1]
    data = yaml.safe_load(fm_text)

    assert data["id"] == "A-01"
    assert "state_marker" in data
