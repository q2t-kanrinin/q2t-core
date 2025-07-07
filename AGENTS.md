# AGENTS.md

**q2t-coreにおける Agent構造と責務分担ガイドライン**

---

## 🧩 なぜ Agent 構造なのか？

q2t-core は構造記述・進化・分類を扱うシステムであり、人間・AI（ChatGPT / Codex）が協調的に関与します。  
この協働関係を明示的に記述するため、各構成要素を「Agent」として定義し、責務を分離・記録します。

---

## 🧠 Agent設計方針

- 1つのAgentは**明確な責務（単一機能）**を持つ
- Agent間のデータ受け渡しは**構造モデル（FoldDSLなど）**を媒介とする
- **人間もAgentの一部**として含める（構造設計・判断・統合）

---

## 🔀 Agent分類と責務一覧

| Agent名 | 概要 | 所属モジュール | φ | ψ | μ |
|---------|------|----------------|---|---|---|
| `HumanAgent` | 構造設計・最終意思決定 | GitHub / Obsidian | ✅ | ✅ | ✅ |
| `ChatGPTAgent` | テンプレレビュー・分類支援・Zettel生成 | 戦略対話 | ✅ | ✅ | △ |
| `CodexAgent` | パーサ・変換器などのコード生成 | `src/`下コード | ✅ | ✅ | ❌ |
| `DSLParser` | Zettelコメント付きFoldDSLを解析 | `src/utils/dsl_parser.py` | ✅ | ✅ | △ |
| `CanvasGenerator`（予定） | Fold構造をObsidian Canvas形式に変換 | `utils/`想定 | ✅ | ✅ | ✅ |
| `TensionTracker`（予定） | テンプレ進化のテンションログを記録・可視化 | `log/` | ❌ | ✅ | ✅ |

---

## 🧭 Agent接続フロー（典型例）

```text
人間（Zettel構造設計）
  ↓
ChatGPTAgent（fold_dslテンプレ初期案生成）
  ↓
CodexAgent（DSLParserやモデルコード実装）
  ↓
DSLParser（fold_dsl-sample.yamlの解析）
  ↓
CanvasGenerator（Obsidian Canvas出力）
  ↓
人間（構造評価・再構築・テンション追加）
  ↓
TensionTracker（進化テンションの記録）
🛡 Agent責務分離規約（構造Linter適用）
src/ 以下には モデル定義のみ 許可（パーサや出力機能は utils/ へ）

tests/ は 単一Agentに対するテストのみ記述可能

Agentを跨ぐ責務が出た場合は BridgeAgent として明示導入すること

📚 今後導入予定のAgent群
Agent名	機能
ASTDiffAgent	テンプレ構造の差分検出（ASTベース）
MacroEvalAgent	fold_macroテンプレの構造評価
ZettelGenAgent	FoldDSL → Zettel群への自動展開
SimLabAgent	テンプレ進化のパターン予測と分類

🧑‍💼 備考：AI Agentとの対話原則（バルサ型構造）
このリポジトリにおける AI Agent は バルサのような即興型支援者として位置づけられます。
人間が「構造設計」と「判断」を担い、AIは「補助生成」と「構造共鳴」に特化します。
→ 詳細は q2tマニフェストまたは構造哲学セクションへ。
