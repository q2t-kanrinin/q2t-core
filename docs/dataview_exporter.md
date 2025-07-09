# Dataview Exporter

このドキュメントでは `src/utils/dataview_exporter.py` を用いて FoldDSL を
Obsidian で扱える Markdown ノートに変換する方法を示します。

## 使い方

```bash
python -m src.utils.dataview_exporter docs/fold_dsl-sample.yaml docs/dataview_sample
```

上記コマンドを実行すると `docs/dataview_sample` ディレクトリに各セクションごとの
Markdown ファイルが生成されます。生成されたノートのフロントマターには
`id`、`title`、`tags`、`state_marker` が含まれます。

生成例 (`A-01.md`):

```markdown
---
id: A-01
title: 抽象
tags: [抽象, 分類, 進化]
state_marker: [phi, psi, mu]
---
抽象概念に関するトップ階層
```

これらのファイルを Obsidian の任意のフォルダにコピーすることで Dataview から参照
可能になります。

## Dataview クエリ例

```dataview
table id, title, state_marker
from "dataview_sample"
```

このクエリを Obsidian 上で実行すると、エクスポートしたノートの一覧を表示できます。
