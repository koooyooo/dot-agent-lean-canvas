# LinkedIn

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
          <li>仕事の信用と人脈が、名刺と履歴書に散らばり、更新されない</li>
          <li>次の仕事を探したいが、求人票と知人紹介だけでは届かない</li>
          <li>採用したい側は、動いていない候補者に、求人媒体だけでは届かない</li>
        </ul>
        <div class="lc-sub"><b>代替</b>
          <ul>
          <li>名刺、履歴書、同窓会名簿、会社のディレクトリ</li>
          <li>求人サイト（Monster 等）、人材紹介、社員紹介</li>
          <li>Facebook 等の私的なSNSで仕事の話をする</li>
        </ul>
        </div>
      </div>
    </td>
    <td colspan="2" class="lc-solution">
      <div class="lc-h">ソリューション</div>
      <div class="lc-b">
        <ul>
          <li>実名の職歴プロフィールを公開し、つながりを可視化できる</li>
          <li>求人と、人づての紹介が、同じグラフの上で届く</li>
          <li>採用側は、プロフィールを検索し、動いていない人にも接触できる</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-uvp">
      <div class="lc-h">UVP</div>
      <div class="lc-b">
        <ul>
          <li>仕事の信用と、次の機会が、ここに揃っている</li>
          <li>例え: 仕事版 Facebook（生きている名刺帳 / 職歴のグラフ）</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-unfair">
      <div class="lc-h">優位性</div>
      <div class="lc-b">
        <ul>
          <li>実名の職歴グラフ（つながりと履歴はコピーしにくい）。採用ワークフローがシートに載ると乗り換えコストになる</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-customer">
      <div class="lc-h">顧客</div>
      <div class="lc-b">
        <ul>
          <li>仕事の顔を持ちたい働く個人（会員。ユーザーであり Premium の顧客でもある）</li>
          <li>採用する企業の人事・採用担当、人材紹介（主に払う顧客）</li>
        </ul>
        <div class="lc-sub"><b>初期</b>
          <ul>
          <li>シリコンバレー周辺のテック職。転職が多く、人脈が仕事そのものになる人</li>
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
          <li>獲得: 新規会員登録、採用側の新規契約</li>
          <li>活性化: プロフィールの職歴入力、最初のつながり、または求人への接触</li>
          <li>継続: MAU、プロフィール更新、採用シートの継続利用</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-channels">
      <div class="lc-h">チャネル</div>
      <div class="lc-b">
        <ul>
          <li>招待、メール、同僚の口コミ</li>
          <li>SEO（実名検索）、採用イベント、後年は Microsoft の到達</li>
        </ul>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="5" class="lc-cost">
      <div class="lc-h">コスト</div>
      <div class="lc-b">
        <ul>
          <li>固定: プロダクト開発、インフラ、信頼・なりすまし対策、本社人件費</li>
          <li>変動: 広告配信、営業、カスタマーサポート、クラウド従量</li>
        </ul>
      </div>
    </td>
    <td colspan="5" class="lc-revenue">
      <div class="lc-h">収益</div>
      <div class="lc-b">
        <ul>
          <li>課金: 採用プロダクト（Recruiter / 求人）が主。広告、会員 Premium が続く</li>
          <li>価格: 採用シートは年額で高額（公開の定価は時期により異なる）。Premium は月額サブスク。いずれも公開LTVはない</li>
          <li>LTV: 未決。会員一人の広告価値より、採用契約の継続が核。公開値はない</li>
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
        <li>数値（採用シート価格、LTV）は公開情報の近似または未決。公式の事業資料として使わない</li>
        <li>会員はユーザーで、採用側が主に払う。会員だけ書くと収益が Premium に偏る。採用だけ書くとプロダクトが履歴書DBになる</li>
        <li>後年の Learning や Sales Navigator、Microsoft 買収後の統合はこのキャンバスの核（職歴グラフと採用）には含めない</li>
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
