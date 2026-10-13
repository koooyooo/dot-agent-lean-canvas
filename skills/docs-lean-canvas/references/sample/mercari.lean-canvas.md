# メルカリ

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
          <li>不用品を、知り合い以外に手間なく売りたいが、出品が重い</li>
          <li>中古をお得に買いたいが、店舗は高く、入札型は面倒</li>
          <li>個人間の送金・未着・偽物が怖く、取引を始められない</li>
        </ul>
        <div class="lc-sub"><b>代替</b>
          <ul>
          <li>Yahoo!オークション</li>
          <li>リサイクルショップ / 質屋</li>
          <li>ジモティー、知人に譲る、捨てる</li>
        </ul>
        </div>
      </div>
    </td>
    <td colspan="2" class="lc-solution">
      <div class="lc-h">ソリューション</div>
      <div class="lc-b">
        <ul>
          <li>スマホで写真を撮ってすぐ出品できる</li>
          <li>アプリ内決済と匿名配送で、会わずに売買できる</li>
          <li>評価・売上金・運営介入で、見知らぬ相手とも取引できる</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-uvp">
      <div class="lc-h">UVP</div>
      <div class="lc-b">
        <ul>
          <li>スマホで、今すぐ売れて、今すぐ買える</li>
          <li>例え: 個人間売買のコンビニ（出品も購入もアプリで完結するフリーマーケット）</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-unfair">
      <div class="lc-h">優位性</div>
      <div class="lc-b">
        <ul>
          <li>出品と購入が揃った流動性（二面市場のネットワーク効果）。ブランド、配送提携、蓄積した評価・取引データ</li>
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-customer">
      <div class="lc-h">顧客</div>
      <div class="lc-b">
        <ul>
          <li>不用品を処分したい個人（売り手）</li>
          <li>中古をお得に買いたい個人（買い手）</li>
        </ul>
        <div class="lc-sub"><b>初期</b>
          <ul>
          <li>スマホネイティブの若年層。ファッションや雑貨を頻繁に入れ替える人</li>
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
          <li>獲得: 新規ダウンロード / 新規登録</li>
          <li>活性化: 初出品、または初購入（どちらか一方で価値を実感）</li>
          <li>継続: MAU、リピート出品率、リピート購入率</li>
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-channels">
      <div class="lc-h">チャネル</div>
      <div class="lc-b">
        <ul>
          <li>アプリストア、口コミ、招待</li>
          <li>SNS、TVCM、交通広告</li>
        </ul>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="5" class="lc-cost">
      <div class="lc-h">コスト</div>
      <div class="lc-b">
        <ul>
          <li>固定: プロダクト開発、インフラ、カスタマーサポート、本社人件費</li>
          <li>変動: 決済手数料、配送関連、広告獲得単価、不正・補償コスト</li>
        </ul>
      </div>
    </td>
    <td colspan="5" class="lc-revenue">
      <div class="lc-h">収益</div>
      <div class="lc-b">
        <ul>
          <li>課金: 出品者からの販売手数料（後年は決済・金融も）</li>
          <li>価格: 販売代金の約10%（初期の公開料率に基づく近似。現行はプランにより異なる）</li>
          <li>LTV: 未決。公開LTVはない。手数料×生涯取引回数から逆算する仮説段階</li>
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
        <li>数値（手数料、LTV）は公開情報の近似または未決。公式の事業資料として使わない</li>
        <li>二面市場なので顧客は売り手と買い手の両方。片方だけ書くとUVPが崩れる</li>
        <li>後年のメルペイ等は当初の約束ではない。このキャンバスはC2Cフリマとしての核に限定している</li>
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
