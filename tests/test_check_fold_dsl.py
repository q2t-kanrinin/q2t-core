from pathlib import Path
import pytest

from src.validators.check_structure import check_fold_dsl


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_unknown_command(tmp_path: Path):
    content = "\n節点 root\n未知 cmd\n"
    path = _write(tmp_path / "sample.dsl", content)
    with pytest.raises(ValueError) as exc:
        check_fold_dsl(str(path))
    assert "未定義の命令語 '未知'" in str(exc.value)


def test_indent_error(tmp_path: Path):
    content = "\n属性 root\n  節点 child\n"
    path = _write(tmp_path / "sample.dsl", content)
    with pytest.raises(ValueError) as exc:
        check_fold_dsl(str(path))
    assert "階層インデントが不正" in str(exc.value)


def test_duplicate_id(tmp_path: Path):
    content = "\n節点 A\n節点 A\n"
    path = _write(tmp_path / "sample.dsl", content)
    with pytest.raises(ValueError) as exc:
        check_fold_dsl(str(path))
    assert "同一ノードID 'A'" in str(exc.value)


def test_empty_node_id(tmp_path: Path):
    content = "\n節点 \n"
    path = _write(tmp_path / "sample.dsl", content)
    with pytest.raises(ValueError) as exc:
        check_fold_dsl(str(path))
    assert "ノードIDが空" in str(exc.value)


def test_undefined_label(tmp_path: Path):
    content = "\n状態 @foo\n"
    path = _write(tmp_path / "sample.dsl", content)
    with pytest.raises(ValueError) as exc:
        check_fold_dsl(str(path))
    assert "未定義のラベル 'foo'" in str(exc.value)

