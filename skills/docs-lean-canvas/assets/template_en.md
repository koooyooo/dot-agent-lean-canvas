<!-- Skeleton for English Lean Canvas. {{token}} is filled by scripts/render.py. Styling by lean-canvas.css. -->
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
      <div class="lc-h">Problem</div>
      <div class="lc-b">
        <ul>
          {{lis_problems}}
        </ul>
        <div class="lc-sub"><b>Existing Alternatives</b>
          <ul>
          {{lis_alternatives}}
        </ul>
        </div>
      </div>
    </td>
    <td colspan="2" class="lc-solution">
      <div class="lc-h">Solution</div>
      <div class="lc-b">
        <ul>
          {{lis_features}}
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-uvp">
      <div class="lc-h">Unique Value Proposition</div>
      <div class="lc-b">
        <ul>
          {{lis_uvp}}
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-unfair">
      <div class="lc-h">Unfair Advantage</div>
      <div class="lc-b">
        <ul>
          {{lis_unfair}}
        </ul>
      </div>
    </td>
    <td rowspan="2" colspan="2" class="lc-customer">
      <div class="lc-h">Customer Segments</div>
      <div class="lc-b">
        <ul>
          {{lis_customers}}
        </ul>
        <div class="lc-sub"><b>Early Adopters</b>
          <ul>
          {{lis_early}}
        </ul>
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="2" class="lc-metrics">
      <div class="lc-h">Key Metrics</div>
      <div class="lc-b">
        <ul>
          {{lis_metrics}}
        </ul>
      </div>
    </td>
    <td colspan="2" class="lc-channels">
      <div class="lc-h">Channels</div>
      <div class="lc-b">
        <ul>
          {{lis_channels}}
        </ul>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="5" class="lc-cost">
      <div class="lc-h">Cost Structure</div>
      <div class="lc-b">
        <ul>
          {{lis_cost}}
        </ul>
      </div>
    </td>
    <td colspan="5" class="lc-revenue">
      <div class="lc-h">Revenue Streams</div>
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
    <td>Type</td>
    <td>{{canvas_type}}</td>
  </tr>
  <tr>
    <td>Canvas Status</td>
    <td>{{status_canvas}}</td>
  </tr>
  <tr>
    <td>Decision</td>
    <td>{{status_decision}}</td>
  </tr>
  <tr>
    <td>Review</td>
    <td>{{cell_review_personal}}</td>
  </tr>
  <tr>
    <td>Investor View</td>
    <td>{{cell_review_investor}}</td>
  </tr>
</table>
