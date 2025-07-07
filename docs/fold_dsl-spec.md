# fold_dsl仕様書 v0.1

## 概要

fold_dsl は、q2t-coreにおけるテンプレ構造・進化テンション・意味ネットワークを  
Zettelベースで表現するための構造記述言語（Domain Specific Language, DSL）である。

---

## 基本構文

### section

```yaml
section:
  id: string       # 一意のID（必須）
  name: string     # ノードの表示名（必須）
  description: string  # ノードの説明（任意）
  tension: integer     # 進化テンション（0〜3）
  children:
    - (sectionオブジェクトの繰り返し)
links
yaml
コードをコピーする
links:
  - source: string
    target: string
    type: string
    weight: float
Foldの階層に加えて、Bridge的なネットワーク構造を表現する要素

meta
yaml
コードをコピーする
meta:
  version: string
  created: string
  author: string
  tags:
    - string
semantic（拡張要素）
yaml
コードをコピーする
semantic:
  keywords:
    - string
  themes:
    - string
バリデーションルール
section.id はユニーク必須

section.name は必須

tension は整数 0〜3

links.source / links.target は section.id と整合

weight は 0.0〜1.0

meta.version は必須

運用方針
Obsidian の FrontMatter としてそのまま埋め込む

YAMLとしての互換性を保つ

Python (PyYAML) で容易にパース可能とする

φψμモデルの拡張がしやすい構造にする

今後の展望
fold_dsl のLinter

fold_dsl のバージョン管理

fold_dsl から Canvas へ自動変換

テンプレ進化のdiff抽出

更新履歴
2025-07-07 v0.1 初稿
