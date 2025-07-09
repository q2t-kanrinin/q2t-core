# q2t-core

**テンプレ進化 × φψμモデル × 構造テンション管理**  
Zettelkasten的知識構造を構文で操作・可視化するオープン構造管理システム

---

## 🧠 What is q2t-core?

q2t-core は、以下の3軸モデルに基づく構造分類・進化テンプレート管理のためのコアシステムです：

- **φ（形式）** FoldDSLによる階層構造の明示化
- **ψ（機能）** テンプレ進化・テンションの追跡と可視化
- **μ（意味）** 意味的タグや文脈によるZettel的知識構造の構築

---

## 🚩 特徴

- Fold（階層）・Bridge（接続）構造をDSLで定義可能
- テンプレ進化を「テンション（進化圧）」として定量記録
- Obsidian / Canvas / GitHubと連携可能
- Zettel準拠の構造記述・履歴追跡・自動マッピング
 - Python / Graphvizベースで可視化可能（semanticタグをツールチップ表示）

---

## 🗂 ディレクトリ構成

docs/ # 仕様・思想・fold_dslサンプル
src/ # パーサ・構造モデル（責務分離）
tests/ # pytestベースのDSL検証コード
log/ # 進化ログ・テンション記録

yaml
コピーする
編集する

---

## 🔧 使用技術

- Python 3.x
- PyYAML / ruamel.yaml
- Pydantic
- Graphviz
- Obsidian Canvas (1.5+)
- Git / GitHub

---

## 🧑‍💻 役割分担（Agent構造）

| 役割 | 概要 |
|------|------|
| 人間 | 最終判断・マージ操作・構造設計 |
| ChatGPT | テンプレレビュー・分類補助 |
| Codex | DSLパーサや構造モデルのコード生成 |

→ 詳しくは [`AGENTS.md`](./AGENTS.md) を参照。

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourname/q2t-core.git
cd q2t-core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # installs PyYAML>=6.0, pydantic>=2.0, ruamel.yaml>=0.18, graphviz>=0.20

# Quick install (once published to PyPI)
pip install q2t-core

# or install via the provided `pyproject.toml`
pip install .

# Parse a DSL file and output JSON to stdout
q2t-parse docs/fold_dsl-sample.yaml

# Export Markdown notes for Dataview
python -m src.utils.dataview_exporter docs/fold_dsl-sample.yaml docs/dataview_sample
# Generate an Obsidian Canvas file
q2t-canvas docs/fold_dsl-sample.yaml canvas_output
q2t-dataview docs/fold_dsl-sample.yaml dataview_output
```

Canvas へのエクスポート方法や詳細オプションは [docs/canvas_generator.md](docs/canvas_generator.md) を参照してください。

### Running Tests

Install the test dependencies and execute the suite:

```bash
pip install -r requirements.txt
# optional extras
pip install .[test]

pytest tests/
```
## 🧭 今後の開発予定
- fold_dslパーサの完全Pydantic化
- テンション可視化ダッシュボード
- テンプレ進化のバージョン履歴管理
- AST構造差分＋テンション流可視化

### 完成済み
- Obsidian Canvasへの構造エクスポート
- Dataview連携用Markdown出力

📜 ライセンスと規範
ライセンス：MIT

行動規範：CODE_OF_CONDUCT.md を参照
