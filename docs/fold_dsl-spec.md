FoldDSL仕様書（fold_dsl-spec.md）

1. 概要と目的

FoldDSLは、q2t-coreにおけるテンプレート構造の記述言語であり、
階層型（Fold）とリンク型（Bridge）の両構造をDSL形式で記述する。

Zettel的知識構造に対応するため、コメント形式でのメタデータ（#title, #tags）も扱う。

この仕様書は、FoldDSLの記述ルール・構文構造・拡張仕様・実行時連携を明文化するものである。

2. FoldDSLの構文構造

#title: Fold構造の例
#tags: [テンプレ, 抽象, 構造]

section:
  id: A-01
  name: 抽象
  description: 上位構造
  tension: 1
  children:
    - id: A-01-01
      name: 概念
      tension: 0
      children: []

links:
  - source: A-01-01
    target: A-01
    type: context
    weight: 0.5

meta:
  version: "0.1"
  created: "2025-07-08"
  author: q2t-admin
  tags: [分類, 進化]

semantic:
  keywords: [抽象, 概念]
  themes: [φψμモデル]

3. 要素定義

🔹 section

id: ノードのユニークID

name: 表示名

description: 任意の説明文

tension: 進化圧（int, default=0）

children: 再帰的に section を持てる

🔹 links

source, target: section.id を指す

type: 任意の語（例: related, context, derived）

weight: 関係の重み（float）

🔹 meta

version, created, author: メタ情報

tags: 分類・用途用タグ（list[str]）

🔹 semantic

keywords: 意味語句（list[str]）

themes: 文脈・分類軸（list[str]）

🔹 コメントヘッダ（Zettel対応）

#title:: 上位タイトル

#tags:: YAML配列形式のタグ

これらは DSLParser により読み取られ、FoldDSLモデルに注入される。

4. state_marker仕様（φψμ進行段階）

state_marker:
  - phi
  - psi
  - mu

判定ルール（CanvasGenerator実装基準）

phi: semantic.keywords が存在する

psi: semantic.themes が存在する

mu: tension > 0 またはリンクに関与

いずれも満たさない場合： state_marker: []

※ state_marker は進行管理マーカーであり、ノードの状態可視化に利用（Obsidian Canvas + Dataview連携）

5. Canvas構造との連携仕様

FoldDSL から Obsidian Canvas (.canvas) に変換する際のマッピング：

FoldDSL属性

Canvasノード

備考

section.id

id

ノード識別子

section.name

label, content

表示名

section.tension

metadata.tension

テンション圧

semantic.keywords/themes

metadata.keywords/themes

意味情報

φψμ座標

metadata.phi/psi/mu

depth, children数, tensionより算出

state_marker

state_marker

進行マーカー（リスト）

6. バージョン管理と互換性

FoldDSLの meta.version により互換性を維持

パーサは常に後方互換性を意識する

今後の拡張候補： examples, ref, annotations, fold_macro など

