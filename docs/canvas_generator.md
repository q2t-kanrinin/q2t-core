# Canvas Generator

`src/utils/canvas_generator.py` を利用して FoldDSL から Obsidian Canvas 用の `.canvas` ファイルを生成する方法を説明します。

## 使い方

1. `DSLParser` で FoldDSL YAML を読み込む
2. `generate_canvas_from_fold_dsl` を呼び出して Canvas データを得る
3. 得られた辞書を JSON として `.canvas` ファイルに保存

### コマンド例

```bash
python - <<'PY'
import json
from src.utils.dsl_parser import DSLParser
from src.utils.canvas_generator import generate_canvas_from_fold_dsl

dsl = DSLParser("docs/fold_dsl-sample.yaml").parse()
canvas = generate_canvas_from_fold_dsl(dsl)

with open("fold_canvas.canvas", "w", encoding="utf-8") as f:
    json.dump(canvas, f, ensure_ascii=False, indent=2)
PY
```

## `.canvas` ファイル構造

生成されるファイルは次の2つのトップレベルキーを持つ JSON です。

- `nodes`: セクションごとのノード一覧
- `edges`: Bridge リンク情報

`nodes` 内の各要素は以下のフィールドを含みます。

- `id` / `label` / `type`
- `x` / `y` 座標 (φ・ψ に基づく)
- `color` (テンション値から自動設定)
- `state_marker` (`phi`, `psi`, `mu` のリスト)
- `metadata` (必要に応じて `tension`, `mu`, `keywords`, `themes` など)

`edges` 内の各要素は `id`, `source`, `target`, `type`, `weight` を持ちます。

作成した `.canvas` ファイルを Obsidian の Canvas プラグイン (1.5+) で開くと、FoldDSL で記述した構造をそのまま可視化できます。
