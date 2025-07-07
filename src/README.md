ChatGPT:
おう、ほなsrc/README.md の叩き台いくで。

✅ src/README.md たたき台
markdown
コードをコピーする
# src - q2t-core

このディレクトリは q2t-core のコアコードを管理します。

---

## コーディング方針

- Python 3.11 以上を推奨
- 型ヒントを必ず記述
- クラスベースの構造を推奨
- φψμの座標情報は必須属性
- fold / bridge は拡張性を意識してモジュール化

---

## フォルダ構成

- `models/`
  - Zettelなどのデータ構造クラス
- `utils/`
  - 汎用関数やヘルパー
- その他必要に応じて追加

---

## テスト

- `pytest` に対応
- テスト対象コードには必ずdocstringを記述
- テストコードは `tests/` に置く

---

## 命名規則

- クラス: CamelCase
- メソッド/関数: snake_case
- 定数: UPPER_SNAKE_CASE

---

## 将来的拡張

- GraphDBへの連携
- YAML/JSONのバリデーション
- φψμの一貫性チェック用Linter
