from pathlib import Path

from src.utils.dsl_parser import DSLParser
from src.utils.tension_tracker import TensionTracker
from src.utils.tension_analyzer import TensionAnalyzer

from tests.test_tension_tracker import create_sample_yaml


def test_tension_analyzer_adjusts(tmp_path: Path) -> None:
    yaml_path = tmp_path / "sample.yaml"
    create_sample_yaml(yaml_path, tension_root=0, tension_child=1)

    parser = DSLParser(str(yaml_path))
    dsl = parser.parse()

    tracker = TensionTracker(log_dir=tmp_path)
    tracker.record(dsl)

    dsl.sections[0].tension = 2
    dsl.sections[0].children[0].tension = 3
    tracker.record(dsl)

    # reset to zero to see adjustment effect
    dsl.sections[0].tension = 0
    dsl.sections[0].children[0].tension = 0

    analyzer = TensionAnalyzer(log_dir=tmp_path)
    analyzer.adjust_fold_dsl(dsl)

    assert dsl.sections[0].tension == 1  # average of [0,2]
    assert dsl.sections[0].children[0].tension == 2  # average of [1,3]
