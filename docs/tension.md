# Tension & Evolution - q2t-core

このドキュメントは、q2t-core における  
**テンション（張力）** と **進化履歴** の管理仕様をまとめます。

---

## テンションとは？

Zettel同士の関係における
- 距離
- つながりの強度
- 進化における緊張度

を数値またはパラメータとして管理する概念。

---

## パラメータ例

- `tension_strength`: 0〜1 の強度
- `update_frequency`: 更新頻度
- `link_age`: リンク生成からの時間
- `evolution_stage`: 進化段階の指標

---

## 記録形式

- JSON / YAML に保存
- ObsidianではDataviewに連携
- 将来的にはGraphDBに移行も視野

---

## テンションの使い道

- 進化の優先順位付け
- フォールドの再編成
- リンクの再構築提案

---

## 進化履歴

Zettelの進化を記録して
- どのバージョンで
- どのテンプレから派生して
- いつ統合されたか

を履歴管理する。

---

## 将来拡張

- テンションの可視化
- 履歴の差分マッピング
- テンション変化のトリガー学習（AI連携）
