ChatGPT:
おう、ほなtests/README.md の叩き台いくで。

✅ tests/README.md たたき台
markdown
コードをコピーする
# tests - q2t-core

このディレクトリは q2t-core のユニットテスト・結合テストを管理します。

---

## テスト方針

- `pytest` を使用
- 主要なモデル・ユーティリティに対してテストを作成
- φψμの属性検証を必ず行う
- fold/bridgeの構造チェックもカバーする

---

## 命名規則

- テストファイル: `test_*.py`
- テストクラス: `Test*`
- テストメソッド: `test_*`

---

## カバレッジ

- カバレッジ計測ツール: coverage.py
- 目標: 80%以上

---

## 実行例

```bash
pytest tests/
