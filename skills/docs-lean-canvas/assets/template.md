<!-- 表の骨格。{{token}} は scripts/render.py が埋める。見た目は lean-canvas.css。 -->
# {{project_name}}

## Lean Canvas

{{blurb}}

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
          {{lis_problems}}
        </ul>
        <div class="lc-sub"><b>代替</b>
          <ul>
          {{lis_alternatives}}
        </ul>
        </div>
      </div>
    </td>
    <td colspan="2" class="lc-solution">
      <div class="lc-h">ソリューション</div>
      <div class="lc-b">
        <ul>
          {{lis_features}}
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-uvp">
      <div class="lc-h">UVP</div>
      <div class="lc-b">
        <ul>
          {{lis_uvp}}
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-unfair">
      <div class="lc-h">優位性</div>
      <div class="lc-b">
        <ul>
          {{lis_unfair}}
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-customer">
      <div class="lc-h">顧客</div>
      <div class="lc-b">
        <ul>
          {{lis_customers}}
        </ul>
        <div class="lc-sub"><b>初期</b>
          <ul>
          {{lis_early}}
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
          {{lis_metrics}}
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-channels">
      <div class="lc-h">チャネル</div>
      <div class="lc-b">
        <ul>
          {{lis_channels}}
        </ul>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="5" class="lc-cost">
      <div class="lc-h">コスト</div>
      <div class="lc-b">
        <ul>
          {{lis_cost}}
        </ul>
      </div>
    </td>
    <td colspan="5" class="lc-revenue">
      <div class="lc-h">収益</div>
      <div class="lc-b">
        <ul>
          {{lis_revenue}}
        </ul>
      </div>
    </td>
  </tr>
</table>

<table class="lc-review" border="1" cellspacing="0" cellpadding="8" style="display:table;width:100%;border-collapse:collapse;">
  <tr>
    <td>種別</td>
    <td>{{canvas_type}}</td>
  </tr>
  <tr>
    <td>キャンバス</td>
    <td>{{status_canvas}}</td>
  </tr>
  <tr>
    <td>決定</td>
    <td>{{status_decision}}</td>
  </tr>
  <tr>
    <td>レビュー</td>
    <td>{{cell_review_personal}}</td>
  </tr>
  <tr>
    <td>投資家視点</td>
    <td>{{cell_review_investor}}</td>
  </tr>
</table>
