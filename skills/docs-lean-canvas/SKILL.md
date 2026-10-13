---
name: docs-lean-canvas
description: >-
  対話または資料から Lean Canvas を作る。YAML を途中保存し、表の Markdown はスクリプトで出す。
  リーンキャンバス、ビジネスモデル、顧客課題、新規事業のやるか、顧客への約束の整理を
  依頼されたときに使う。地図の完成と投資決定は分ける。Amazon の PR/FAQ が担う入口はここ。出荷 PRD は docs-prd。
---

# Lean Canvas 作成

対話または提供資料からキャンバスを埋める。一度に完成させなくてよい。
事業として成立しにくい項目があれば、その場で伝える。

新規の賭けで「誰に何を約束し、どう儲けるか」を固定する。やるかはキャンバスを描いたうえで決める。地図の完成（`status_canvas`）と決定（`status_decision`）は分けて書く。`status_decision` は個人のやるかであり、投資家の Go ではない。Amazon の PR/FAQ が担う入口はここ（プレスリリースは書かない。UVP と顧客・収益で約束を立てる）。既存機能の次の課題は `docs-prd` の intercom。投資決定後の横断出荷は `docs-prd` の google。

## 入力

以下を確認する
- 対象（プロダクト / サービス名）
- 保存先:
  - ユーザーからの明示的な保存先指定があればそれを最優先する。
  - 未指定の場合、環境変数 `LEAN_CANVAS_OUTPUT_DIR` が設定されていればそのディレクトリ配下に保存する。
  - どちらも無ければ、保存先ディレクトリをユーザーに確認する（カレントディレクトリ等）。
  - YAML を正本、同名の Markdown をスクリプトによる派生物として管理する。途中版を同じ場所に保存しても、完成や実行決定を推定せず実際のステータスを維持する。

## 手順

1. [assets/template.yaml](assets/template.yaml) を読む
2. `{slug}.lean-canvas.yaml` を保存する。既存ファイルは上書きしない。`canvas_type` を確認する（自分の賭けなら `New`、既存の分解・教材なら `PostHoc`）。途中なら `status_canvas: Draft` または `Building`。決定していなければ `status_decision: Undecided`
3. 不足を聞き、YAML を更新する
4. レビューを二つ書く。本体（表の「レビュー」）は下の「よくある崩れ」を見て `review_personal` に出す。投資家視点は必ず [references/review-investor.md](references/review-investor.md) を読んでから `review_investor` に出す。ユーザーが価値を感じない、継続して利用されない、事業として成立しにくい、等があれば本体のレビューで誠実に伝える。`canvas_type: New` なら穴は「未決と理由」。`PostHoc` なら結果からの再構成であり、当時の成功を今の `Go` にしない。よくある崩れと投資家視点は、この場合どちらの欄の主にもしない
5. `status_canvas: Done` になったとき、または出力を求められたときは、表を手で組まない。スキルディレクトリの [scripts/render.py](scripts/render.py) を、次の順で最初に成功したインタプリタで走らせる（Windows は `py -3` を先に）。引数は YAML。未指定なら同名の `{slug}.lean-canvas.md` を出す。表の骨格は [assets/template.md](assets/template.md)（英語時は [assets/template_en.md](assets/template_en.md)）、見た目は [assets/lean-canvas.css](assets/lean-canvas.css) をスクリプトが読む。CSS は編集用の正本として保持し、生成時に各 HTML 要素の `style` 属性へ展開する。出力は外部 CSS、`class`、`<link>`、`<style>` に依存せず、CSS ファイルをコピーしない。Markdown 出力の条件は `status_canvas` であり、`status_decision` ではない
   - `py -3`
   - `python3`
   - `python`
   - 例（スキルディレクトリを作業ディレクトリにして `terminal` で実行）: `python3 scripts/render.py /path/to/{slug}.lean-canvas.yaml`
   - どれも無い、またはスクリプトが失敗したときは、理由を報告し、既存の派生 Markdown を壊さず YAML を保持する。手動出力が必要な場合だけ言語別テンプレートの同じ 5 列構造を使い、CSS の該当宣言を `style` 属性へ展開する。外部 CSS や `<style>` に戻さない。展開を検証できなければ、装飾なしの代替出力であることを明示し、対応済みとは報告しない。

## 書き方

- YAML のプレースホルダ文は成果物に残さない。分からないマスは空より「未決」と理由
- `status_canvas` は地図として読めるか（`Draft` / `Building` / `Done`）。`status_decision` はそれを見て今やるか（`Undecided` / `Go` / `NoGo` / `Parked`）。検証済みフラグではない。個人の決定であり、投資家欄の結論ではない。`Parked` は今はやらない。方針を変えるときはキャンバスを書き `iteration` を上げ、決定は `Undecided` に戻す
- `status_decision: Go` のときは表の「レビュー」に、何を見て Go にしたかを1行残す（まだ仮説、顧客の声、自分の制約など）
- `PostHoc` でこのキャンバス自体を賭けないとき（教材・既存分解）は `status_canvas` と `status_decision` を `-` にする。マスが埋まっても投資決定ではない。`Go` にしない
- Markdown の 5 列 HTML は [scripts/render.py](scripts/render.py) が [assets/template.md](assets/template.md) と [assets/lean-canvas.css](assets/lean-canvas.css) から出す。表の形を変えるときは template.md と CSS を直し、Python の表ハードコードは触らない。種別・キャンバス・決定・レビュー・投資家視点はキャンバス表に入れず、下の表に出す。手組みするときだけ template.md の `{{…}}` を埋める。CSS は `<style>` ブロックではなく各要素の `style` 属性に展開する。表はネストしない。空白セルや 3 列にしない
- YAML の配列と指標・コスト・収益・UVP はセル内を `<ul>` にする。UVP は headline と「例え: high_level_concept」の2項目（スクリプトがそう出す）
- UVP の headline は顧客に聞こえる約束にする。機能一覧の要約にしない
- マスの書き方の後追い例（公式見解ではない）: [メルカリ](references/sample/mercari.lean-canvas.yaml)、[YouTube](references/sample/youtube.lean-canvas.yaml)、[LinkedIn](references/sample/linkedin.lean-canvas.yaml)。評価観点の基準にしない
- ユーザーの言語に合わせる。英語出力時は YAML の `meta.lang: en` を指定する（未指定なら `ja`）。`render.py` が自動で英語テンプレート（[assets/template_en.md](assets/template_en.md)）と英語ラベル（Problem, Acquisition:, Fixed: 等）に切り替える（CLI オプション `--lang en` でも指定可）

## Markdown ビューアー互換性

- 標準出力は自己完結した HTML 表入り Markdown。罫線、背景・文字色、余白、リスト、列幅を inline style に展開し、クラスを除去する。既存のコピー済み CSS は不要だが、ユーザーのファイルは削除しない。
- [scripts/inline_css.py](scripts/inline_css.py) は依存なしの限定 CSS 展開器。タグ・クラスの複合指定、子孫、カンマ区切り、`:first-child` / `:last-child`、詳細度・宣言順・既存 style・`!important` を扱う。ショートハンドと個別プロパティの順序を維持するため、出力に宣言の重複が残る場合がある。
- 対応プロパティは展開器の `PROPERTIES` に列挙。値は単純な色・寸法・キーワード・非引用フォント列などに限定する。子結合子、属性セレクタ、その他の疑似クラス、at-rule、CSS 関数・変数、引用値、未対応プロパティはエラーにする。CSS を拡張するときは先に回帰テストと対応を追加し、黙って落とさない。汎用 CSS エンジンや値の完全な妥当性検証ではない。
- `--css-src` は展開元 CSS の指定。旧 `--css-href` / `--no-copy-css` は互換用に受け付けるが効果はない。`--template` は明示的な閉じタグを持つ HTML テンプレートを指定し、`<link>` / `<style>` は置かない。
- テンプレートの改行・インデントは削らず、表の `white-space: normal` で編集ビューの `pre-wrap` / `pre-line` 継承を止める。空白が行ボックスになると見出し前とリスト間が広がる。セルの `vertical-align: top !important` も維持する。テーマの `middle !important` に負けると内容量・rowspan に応じて見出し位置がばらつく。二つの症状を分けて再現し、本文の改行を正規表現で一括削除して直さない。
- Obsidian の HTML サニタイズ（https://obsidian.md/help/html）と Typora の編集表示制約（https://support.typora.io/HTML/）を考慮しても、全テーマ・全プロパティの同一表示は保証しない。クラスをテーマに置くだけで解決すると案内しない。YAML→MD の生成検証と、実アプリの編集・閲覧・印刷表示の確認は区別する。

## 検証

- スキルディレクトリで `terminal` から `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` を実行する（Windows は環境変数を相応の方法で設定）。日英 CLI、エスケープ、5 列構造、子孫・先頭末尾セル、カスケード、未対応 CSS の失敗を確認する。
- レイアウト変更時は [tests/test_layout_browser.py](tests/test_layout_browser.py) も実行する。別の仮想環境へ `python -m pip install playwright`、`python -m playwright install chromium` を `terminal` で実行して準備し、その Python で上記 unittest を走らせる。インストール済み Chrome を使う場合は `LEAN_CANVAS_BROWSER_CHANNEL=chrome` を設定する。日英 × normal / pre-wrap / pre-line × 通常 / middle !important のブラウザー実測で見出し上端・リスト間隔・表高・本文・5 列 rowspan を確認する。Playwright 未導入時はこのテストだけ skip されるため、通常テスト成功だけをレイアウト検証と数えない。継承の試験 HTML は `<!doctype html>` を付ける（quirks mode の table の既定動作では不具合を見逃す）。
- 再出力時は YAML の変更前後ハッシュを比較し、生成 Markdown に `<link>` / `<style>` / `class=` がなく、元の内容と 5 列構造が保たれていることを確認する。アプリを開いていない場合は UI 未検証と報告する。

## よくある崩れ（レビュー用）

合格判定でも `status_decision` でもない。YAML にチェック欄は作らない。見た結果は `review_personal` にだけ出す。投資家用の観点ファイルは作らず、ここが正本。

見るもの:

- 課題より先にソリューションだけ詳しい
- 代替が空、または「特に何もしていない」だけ
- 顧客が「全員／すべての企業」で、初期がいない
- UVP が機能一覧・スローガンで、顧客に聞こえる約束になっていない
- チャネルが「SNS／口コミ」だけで、最初の到達がない
- 困る人と払う人が違うのに、キャンバス上で区別していない

出し方:

- 該当した崩れと、該当しそうだが今回は違うと言えるものだけ書く
- 全部見えないなら「よくある崩れは今回見えない」の1行でよい。6行の OK リストは出さない
- 該当が多くても自動で `NoGo` にしない。成立しない論理だけ人が `NoGo` する
- 優位性が空なこと自体は初期では普通なので、このリストには入れない
