![logo](./logo.jpg)

# dot-agent-lean-canvas

[English](README.md) | **日本語**

AI エージェント向けの Lean Canvas（リーンキャンバス）作成・レビュー用スキルです。
YAML を正本として管理し、外部 CSS やプラグインに依存しない自己完結した HTML テーブル（インライン style 展開済み）を含む Markdown を生成します。

---

![リーンキャンバス出力例（YouTube ケーススタディ）](sample_output.png)

> **免責事項**: 上記のリーンキャンバスは、出力フォーマットの例示および学習目的のために、公開情報をもとに作成した YouTube の後追いケーススタディです。YouTube または Google LLC による公式な文書・開示資料ではありません。記載されている製品名・ロゴ・ブランド等は各権利者に帰属します。

---

## 特徴

- **エージェント駆動のリーンキャンバス作成**:
  - 対話や資料から仮説を埋め、ビジネスモデルの構造（課題・顧客・UVP・チャネル・収益等）を整理。
  - 地図の完成度（`status_canvas`）と本人の実行判断（`status_decision`）を分離して管理。
- **二重のレビュー視点**:
  - **自己レビュー（`review_personal`）**: よくある論理崩れ（課題なきソリューション、代替の欠如など）の点検。
  - **投資家視点（`review_investor`）**: 外部資本の観点から市場性やトラクション仮説、脆いポイントを点検。
- **ポータブルな Markdown 出力**:
  - 公式の 5 列構成（課題・顧客が両端、UVP が中央）を維持。
  - GitHub、Obsidian、VS Code、Typora などの Markdown ビューアーで崩れず表示できるよう、CSS プロパティをインライン展開。
- **外部依存ゼロ**:
  - Python 3 の標準ライブラリのみで動作（サードパーティ製パッケージのインストール不要）。
- **日英バイリンガル対応**:
  - 日本語（`lang: ja`）および英語（`lang: en`）の出力に対応。

---

## ディレクトリ構成

```text
.
├── install.sh                  # ~/.agents/skills/ へのシンボリックリンク作成スクリプト
├── sample_output.png           # リーンキャンバス出力例のプレビュー画像
├── README.md                   # 英語ドキュメント
├── README_ja.md                # 日本語ドキュメント（本ファイル）
├── LICENSE                     # CC BY-NC 4.0 ライセンス
└── skills/
    └── docs-lean-canvas/
        ├── SKILL.md            # エージェント用指示書（スキル定義）
        ├── assets/
        │   ├── template.yaml   # リーンキャンバス YAML テンプレート
        │   ├── template.md     # 表骨格テンプレート（日本語）
        │   ├── template_en.md  # 表骨格テンプレート（英語）
        │   └── lean-canvas.css # スタイリング定義（生成時にインライン化）
        ├── references/
        │   ├── review-investor.md  # 投資家視点のレビュー基準
        │   └── sample/         # 後追いサンプル（メルカリ、OpenAI、LinkedIn、YouTube）
        ├── scripts/
        │   ├── render.py       # YAML -> Markdown 変換スクリプト
        │   └── inline_css.py   # CSS インライン展開器
        └── tests/
            ├── test_render.py  # 変換処理・エスケープ等のユニットテスト
            └── test_layout_browser.py # Playwright によるレイアウト回帰テスト（任意）
```

---

## インストール

`install.sh` は macOS / Linux を前提としています。Windows では WSL 上で実行してください。

本リポジトリのスキルを `~/.agents/skills/docs-lean-canvas` へシンボリックリンクします。

```bash
# 事前確認（dry-run）
./install.sh --dry-run

# インストール実行
./install.sh
```

> **注意**: `install.sh` のインストール先は `~/.agents/skills/` 配下です。Cursor と Codex はこのディレクトリを直接読み込むため、追加の設定は不要です。お使いのエージェントが別のディレクトリからスキルを読み込む場合は、利用中の環境に応じて配置先を変更するか、そのディレクトリからシンボリックリンクを貼ってください。例:
>
> ```bash
> # Claude Code（~/.claude/skills/）
> mkdir -p ~/.claude/skills
> ln -s ~/.agents/skills/docs-lean-canvas ~/.claude/skills/docs-lean-canvas
>
> # Antigravity / Antigravity IDE / Antigravity CLI（~/.gemini/config/skills/）
> mkdir -p ~/.gemini/config/skills
> ln -s ~/.agents/skills/docs-lean-canvas ~/.gemini/config/skills/docs-lean-canvas
> ```

---

## 使い方

### 1. AI エージェント（Cursor, Antigravity など）での利用

エージェントに対して以下のように依頼します：

> 「〇〇というプロダクトのアイディアがあるので、リーンキャンバスを作ってほしい」

対応しているエージェントでは、`/docs-lean-canvas` のようにスラッシュコマンドで明示的に呼び出すこともできます（呼び出し方はエージェントによって異なります）。

エージェントが `skills/docs-lean-canvas/SKILL.md` の指示に従い、対話を通じて `{slug}.lean-canvas.yaml` を作成・更新し、`render.py` を呼び出して `{slug}.lean-canvas.md` を生成します。

#### 保存先の設定
- プロンプトで明示的に指定した場合（例: `docs/ideas/ に保存して`）はその指定が最優先されます。
- 常に出力先を固定したい場合（Obsidian vault 配下など）、環境変数 `LEAN_CANVAS_OUTPUT_DIR` を設定しておくと自動でその配下に出力されます：
  ```bash
  export LEAN_CANVAS_OUTPUT_DIR="$HOME/ObsidianVault/business/idea"
  ```
- 環境変数がなく保存先の指定もない場合は、エージェントが都度保存先を確認します。

### 2. 手動での Markdown 生成（CLI）

YAML ファイルから手動で Markdown を生成することも可能です。

```bash
# 基本実行（同名の .md が出力されます）
python3 skills/docs-lean-canvas/scripts/render.py path/to/my-product.lean-canvas.yaml

# 出力先を指定する場合
python3 skills/docs-lean-canvas/scripts/render.py path/to/my-product.lean-canvas.yaml path/to/output.md

# 英語テンプレートで出力する場合
python3 skills/docs-lean-canvas/scripts/render.py path/to/my-product.lean-canvas.yaml --lang en
```

---

## テストの実行

Python 3 の標準機能でユニットテストを実行できます：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/docs-lean-canvas/tests -v
```

---

## ライセンス

本リポジトリは [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](LICENSE) のもとで公開されています。非営利目的での利用・改変・共有は自由ですが、商用利用は禁止されています。
