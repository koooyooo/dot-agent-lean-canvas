# OpenAI

## Lean Canvas

既存サービスの後追いサンプル。公式資料ではない。

<link rel="stylesheet" href="../../assets/lean-canvas.css">

<table class="lc" border="1" cellspacing="0" cellpadding="0" style="display:table;width:100%;border-collapse:collapse;table-layout:fixed;">
  <colgroup>
    <col style="width:10%"><col style="width:10%">
    <col style="width:10%"><col style="width:10%">
    <col style="width:10%"><col style="width:10%">
    <col style="width:10%"><col style="width:10%">
    <col style="width:10%"><col style="width:10%">
  </colgroup>
  <tr>
    <td rowspan="2" colspan="2" class="lc-problem">
      <div class="lc-h">課題</div>
      <div class="lc-b">
        <ul>
          <li>文章・コード・調査が要るが、専門家に頼むのも、検索して自分でまとめるのも重い</li>
          <li>プロダクトに言語の知能を載せたいが、基盤モデルの学習も運用も自前では届かない</li>
          <li>企業は使いたいが、品質・権限・データの扱いが保証されないと業務に載せられない</li>
        </ul>
        <div class="lc-sub"><b>代替</b>
          <ul>
          <li>検索、Wikipedia、Stack Overflow、社内Wiki、外注のライター / エンジニア</li>
          <li>自前のNLP、オープンな重み、他社のクラウドAI API</li>
          <li>使わない、シャドーITの個人アカウント、専用の業務SaaS</li>
        </ul>
        </div>
      </div>
    </td>
    <td colspan="2" class="lc-solution">
      <div class="lc-h">ソリューション</div>
      <div class="lc-b">
        <ul>
          <li>チャットで頼めば、下書き・説明・コードがすぐ返る</li>
          <li>同じ系統のモデルを、APIのトークン課金で自分のアプリに埋め込める</li>
          <li>有料プランと法人向けで、上限・管理・データ取り扱いを業務向けに揃えられる</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-uvp">
      <div class="lc-h">UVP</div>
      <div class="lc-b">
        <ul>
          <li>聞いて、すぐ使える知能がある</li>
          <li>例え: 言語の電力会社（コンセントにつなげば、対話も埋め込みもできる汎用モデル）</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-unfair">
      <div class="lc-h">優位性</div>
      <div class="lc-b">
        <ul>
          <li>学習と推論の規模、ChatGPT から入る利用データとブランド。Microsoft 経由の計算資源と資本。後発は同じ前計算を買い直せない</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-customer">
      <div class="lc-h">顧客</div>
      <div class="lc-b">
        <ul>
          <li>調べて書いて作りたい個人（ユーザー。Plus では払う顧客でもある）</li>
          <li>アプリに知能を載せたい開発者・スタートアップ（APIの払う顧客）</li>
          <li>全社で使わせたい企業のIT / 事業部門（法人契約の払う顧客）</li>
        </ul>
        <div class="lc-sub"><b>初期</b>
          <ul>
          <li>GPT-3 API のウェイティングリストに並んだ開発者。その後、ChatGPT を先に触ったテック慣れした個人</li>
        </ul>
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="2" class="lc-metrics">
      <div class="lc-h">主要指標</div>
      <div class="lc-b">
        <ul>
          <li>獲得: ChatGPT の新規登録、API の新規キー / 新規有料契約</li>
          <li>活性化: 初めて役に立つ返答を得た（チャット完了、または API の本番リクエスト）</li>
          <li>継続: 週次の利用、Plus / API の継続課金、法人シートの更新</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-channels">
      <div class="lc-h">チャネル</div>
      <div class="lc-b">
        <ul>
          <li>プロダクトそのものの拡散（ChatGPT）、開発者向けドキュメントと API</li>
          <li>口コミ、X、研究ブログ、Microsoft のクラウドと GitHub 経由の到達</li>
        </ul>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="5" class="lc-cost">
      <div class="lc-h">コスト</div>
      <div class="lc-b">
        <ul>
          <li>固定: 研究、プロダクト、安全・信頼性、本社人件費</li>
          <li>変動: 学習と推論の計算、帯域、企業サポート、パートナー分配</li>
        </ul>
      </div>
    </td>
    <td colspan="5" class="lc-revenue">
      <div class="lc-h">収益</div>
      <div class="lc-b">
        <ul>
          <li>課金: ChatGPT のサブスクと法人、API のトークン従量。後年は周辺プロダクトも</li>
          <li>価格: Plus は月額約 $20 前後の公開価格。API はモデルとトークン単価が公開され、時期で変わる。法人は非公開が多い</li>
          <li>LTV: 未決。公開LTVはない。個人サブスクと API の従量を混ぜると一人あたりの意味が消える</li>
        </ul>
      </div>
    </td>
  </tr>
</table>

<table class="lc-review" border="1" cellspacing="0" cellpadding="8" style="display:table;width:100%;border-collapse:collapse;">
  <tr>
    <td>種別</td>
    <td>PostHoc</td>
  </tr>
  <tr>
    <td>キャンバス</td>
    <td>-</td>
  </tr>
  <tr>
    <td>決定</td>
    <td>-</td>
  </tr>
  <tr>
    <td>レビュー</td>
    <td>
      <ul>
        <li>既存サービスの後追いである。初期の仮説検証ではなく、結果からマスを埋めている。status_canvas / status_decision は -。当時の成功を今の Go にしない</li>
        <li>核は ChatGPT と API（言語の知能を使う / 埋め込む）。非営利の研究ラボとして始まった約束や、後年の動画・エージェント・ハードは含めない</li>
        <li>困る人（個人・開発者のユーザー）と払う人（Plus、API、法人）を分けた。無料利用者だけ書くと収益が消える。APIだけ書くとプロダクトが開発者基盤になる</li>
        <li>数値（Plus価格、LTV）は公開情報の近似または未決。公式の事業資料として使わない</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>投資家視点</td>
    <td>
      <ul>
        <li>教材の後追いであり、この欄の主にしない。後年の時価や調達額を当時の投資判断にしない</li>
      </ul>
    </td>
  </tr>
</table>
