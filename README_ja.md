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
  - 検証の結果を伝えると、キャンバスを直し、`iteration` を上げ、判断を `Undecided` に戻して、次に脆い仮説を選び直します。
- **リスク基準のレビュー（Running Lean）**:
  - **3 つのリスク（`review_risks`）**: 顧客・市場・プロダクト（課題・解決策）の各リスクに、証拠の強さ（`Untested` / `Signal` / `Supported` / `Refuted`）と一言コメントを記載。実在の競合と価格帯、ユーザーの生の不満で裏付け。
  - **検証段階（`review_stages`）**: 課題／解決策フィット・製品／市場フィット・拡大の各段階に、状態とクリアの根拠（または残りの課題）を一言で記載。必要なリスクが `Supported` でなければ `Cleared` にできず、`render.py` が警告。
  - **最も脆い仮説（`review_fragile_hypothesis`）**: どのリスクの仮説かを添えて 1 つ特定し、数時間〜1 週間でできる具体的な検証アクションを 1 つ提案。
  - **ランクと総評（`review_rank`・`review_personal`）**: 見込みによる S〜D の評価と、一番弱いリスクを挙げた理由（課題／解決策フィット前の S・A には「見込み・未検証」を付記）。続けて、よくある論理崩れの点検と任意のローカル評価基準（`custom-policy-{name}.md`）を記載。
  - レビューはキャンバスの下に、メタ情報・リスク・検証・総評（ランク／一言／所見）の 4 つの表で出力。
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
        │   ├── custom-policy-template.md # ローカル評価基準（カスタムポリシー）のテンプレート
        │   ├── maintenance.md  # 保守者向け: 描画処理・ビューア互換性・検証手順
        │   ├── review-rank.md      # ランク（S〜D）の評価基準
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

本リポジトリを clone し、スキルを `~/.agents/skills/docs-lean-canvas` へシンボリックリンクします。

```bash
# 1. 残しておく場所に clone する（シンボリックリンクはこのディレクトリを指します）
git clone https://github.com/koooyooo/dot-agent-lean-canvas.git
cd dot-agent-lean-canvas

# 2. 事前確認（dry-run）
./install.sh --dry-run

# 3. インストール実行
./install.sh
```

clone 先を移動・削除するとリンクが切れます。更新は `git pull` で反映されます。

### エージェントごとの設定

`install.sh` のインストール先は `~/.agents/skills/` 配下です。お使いのエージェントが別のディレクトリからスキルを読み込む場合は、利用中の環境に応じて配置先を変更するか、そのディレクトリからシンボリックリンクを貼ってください。

#### Cursor / Codex

`~/.agents/skills/` を直接読み込むため、追加の設定は不要です。

#### Claude Code

```bash
mkdir -p ~/.claude/skills
ln -s ~/.agents/skills/docs-lean-canvas ~/.claude/skills/docs-lean-canvas
```

#### Antigravity / Antigravity IDE / Antigravity CLI

```bash
mkdir -p ~/.gemini/config/skills
ln -s ~/.agents/skills/docs-lean-canvas ~/.gemini/config/skills/docs-lean-canvas
```

#### Hermes Agent

```bash
mkdir -p ~/.hermes/skills/custom
ln -s ~/.agents/skills/docs-lean-canvas ~/.hermes/skills/custom/docs-lean-canvas
```

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
- 環境変数がなく保存先の指定もない場合は、エージェントが `1.` カレントディレクトリ、`2.` `~/Documents/lean-canvas/`、`3.` その他のパス、から番号で選ぶよう確認します。保存先のディレクトリがなければ作成します。

#### カスタム評価基準（Custom Policy）の設定（任意）
`skills/docs-lean-canvas/references/custom-policy-template.md` をコピーして `skills/docs-lean-canvas/references/custom-policy-{name}.md` を作成することで、独自の評価基準（個人開発・NoOps制約、目標収益ラインなど）を追加できます。
- `custom-policy-template.md` 以外の `custom-policy-*.md` は `.gitignore` 対象となっており、非公開の判断基準がリポジトリに混入しません。
- `custom-policy-{name}.md` が 1 つ存在する場合は既定で読み込まれ、`review_personal` と `review_rank` のレビューに自動反映されます。

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
