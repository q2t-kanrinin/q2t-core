# q2t-core

φψμモデルに基づく  
**テンプレ進化・構造分類のZettel管理システム**  

---

## 概要

q2t-core は  
- Fold（階層型構造）  
- Bridge（ネットワーク型構造）  
のテンプレート進化を  
「テンション」という進化圧の概念で記録し、  
Zettel的に再構築・追跡できるオープン構造管理プラットフォームです。

---

## 特徴

- φψμ（形式・機能・意味）の3軸モデル
- fold_dsl によるテンプレ構造のDSL定義
- Obsidian / GitHub / Canvasと連携可能
- テンション（進化圧）の定量評価
- バージョン管理・履歴管理をGitベースで運用

---

## ディレクトリ構成

```plaintext
docs/      # 仕様・思想・DSL
src/       # fold_dslパーサ・周辺モジュール
log/       # 進行ログ
tests/     # テストコード
使用技術
Python 3.x

PyYAML

Graphviz

Obsidian Canvas

GitHub

役割分担
人間: 最終判断、GitHubマージ

ChatGPT: 仕様レビュー

Codex: コード生成

詳しくは AGENTS.md を参照。

Getting Started
bash
コピーする
編集する
git clone https://github.com/yourname/q2t-core.git
cd q2t-core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
今後の開発予定
fold_dslパーサのpydantic化

Canvasエクスポート

テンションの可視化ダッシュボード

テンプレ進化のバージョン管理

ライセンス
MIT
コミュニティ行動規範は [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) を参照してください。
