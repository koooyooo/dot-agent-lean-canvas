# YouTube

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
          <li>見たい映像があるが、放送時刻やレンタルに縛られ、すぐ観られない</li>
          <li>自分の映像を公開したいが、ホスティングもエンコードも共有も重い</li>
          <li>広告主は、テレビほど高くなく、興味のある人の近くに出したい</li>
        </ul>
        <div class="lc-sub"><b>代替</b>
          <ul>
          <li>テレビ、レンタルビデオ / DVD</li>
          <li>自前サーバ、ファイル共有、Google Video、Vimeo</li>
          <li>テレビCM、バナー広告、検索連動広告</li>
        </ul>
        </div>
      </div>
    </td>
    <td colspan="2" class="lc-solution">
      <div class="lc-h">ソリューション</div>
      <div class="lc-b">
        <ul>
          <li>ブラウザで、探した動画をすぐ再生できる</li>
          <li>アカウントがあれば、誰でも動画を上げて公開できる</li>
          <li>視聴の横に広告を出し、投稿者と分配できる</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-uvp">
      <div class="lc-h">UVP</div>
      <div class="lc-b">
        <ul>
          <li>見たい映像が、今すぐ見つかって、今すぐ観られる</li>
          <li>例え: 動画版 Flickr（誰でも上げて、誰でも見られる動画共有）</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-unfair">
      <div class="lc-h">優位性</div>
      <div class="lc-b">
        <ul>
          <li>視聴・投稿・索引が揃ったカタログのネットワーク効果。Google 経由の到達。蓄積した視聴データと投稿者のファンベース</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-customer">
      <div class="lc-h">顧客</div>
      <div class="lc-b">
        <ul>
          <li>動画を観たい個人（視聴者。ユーザー）</li>
          <li>動画を上げて見てもらいたい個人・媒体（投稿者。供給）</li>
          <li>その注意を買いたい広告主（払う顧客）</li>
        </ul>
        <div class="lc-sub"><b>初期</b>
          <ul>
          <li>短いクリップをメールや掲示板より楽に共有したい、ネット慣れした個人</li>
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
          <li>獲得: 新規視聴（未ログイン含む）、新規投稿アカウント</li>
          <li>活性化: 初回の再生完了、または初投稿</li>
          <li>継続: 視聴時間、再訪、投稿の継続。後年はウォッチタイムが核</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-channels">
      <div class="lc-h">チャネル</div>
      <div class="lc-b">
        <ul>
          <li>埋め込み、URL共有、検索、関連動画</li>
          <li>Google 検索とプロパティ。口コミ</li>
        </ul>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="5" class="lc-cost">
      <div class="lc-h">コスト</div>
      <div class="lc-b">
        <ul>
          <li>固定: プロダクト、インフラ、モデレーション、本社人件費</li>
          <li>変動: 配信帯域、ストレージ、広告配信、投稿者への収益分配</li>
        </ul>
      </div>
    </td>
    <td colspan="5" class="lc-revenue">
      <div class="lc-h">収益</div>
      <div class="lc-b">
        <ul>
          <li>課金: 広告（視聴の注意を広告主に売る。後年は Premium も）</li>
          <li>価格: 広告単価は CPM / 視聴単価で案件により大きく異なる。公開の一律価格はない</li>
          <li>LTV: 未決。公開LTVはない。視聴者一人ではなく、広告主の出稿と投稿者の在庫で逆算する</li>
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
        <li>数値（広告単価、LTV）は公開情報の近似または未決。公式の事業資料として使わない</li>
        <li>視聴者はユーザー、投稿者は供給、広告主が払う顧客。視聴者だけ書くと収益が消える。広告主だけ書くとプロダクトが広告枠になる</li>
        <li>後年の Shorts、Premium、TV はこのキャンバスの核（UGC動画と広告）には含めない</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>投資家視点</td>
    <td>
      <ul>
        <li>教材の後追いであり、この欄の主にしない。後年の規模や時価を当時の投資判断にしない</li>
      </ul>
    </td>
  </tr>
</table>
