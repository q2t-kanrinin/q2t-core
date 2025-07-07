from pathlib import Path

from src.validators.check_structure import check_fold_dsl


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_unknown_command(tmp_path: Path, capsys):
    content = "\n節点 root\n未知 cmd\n"
    path = _write(tmp_path / "sample.dsl", content)
    check_fold_dsl(str(path))
    captured = capsys.readouterr().out
    assert "未定義の命令語 '未知'" in captured


def test_indent_error(tmp_path: Path, capsys):
    content = "\n属性 root\n  節点 child\n"
    path = _write(tmp_path / "sample.dsl", content)
    check_fold_dsl(str(path))
    captured = capsys.readouterr().out
    assert "階層インデントが不正" in captured


def test_duplicate_id(tmp_path: Path, capsys):
    content = "\n節点 A\n節点 A\n"
    path = _write(tmp_path / "sample.dsl", content)
    check_fold_dsl(str(path))
    captured = capsys.readouterr().out
    assert "同一ノードID 'A'" in captured

