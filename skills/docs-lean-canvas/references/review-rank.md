# Rank Review (`review_rank`)

Read before writing `review_rank` for `New` canvases. The rank is the evaluator's grade of this canvas's **prospect**: how promising it is if its hypotheses hold. It is not map completeness (`status_canvas`), not evidence (that is `review_risks` / `review_stages`), and not the user's personal decision (`status_decision`).

Canvas examples (`references/sample/`) demonstrate how to fill in boxes and should not be used as benchmarks for this file. Do not grade an idea by later-stage outcomes of similar companies.

## Grades

| Grade | Meaning | Judgment |
|---|---|---|
| S | Outstanding (commit) | Market, revenue, and feasibility all look strong; worth executing now |
| A | Strong (adopt with conditions) | The core line holds; adopt on condition of addressing specific, minor risks |
| B | Standard (revise / hold) | The idea is good, but grounds (e.g., numbers, customer evidence) are weak; needs brushing up |
| C | Pass (major rework) | Premises or market research are lacking; the business model needs fundamental rethinking |
| D | Reject | Feasibility is extremely low, or it does not fit the strategy at all |

## How to Grade

- Grade by prospect, not by evidence. Evidence is shown in the risk and stage rows; do not cap the grade by stage.
- `reason` is one line and must name the weakest risk (customer, market, or product), e.g., "A: The problem is strong and willingness to pay looks plausible from competitor pricing, but reaching early adopters is the weakest point."
- `render.py` appends "(prospect, unverified)" ("（見込み・未検証）" in Japanese) to S or A while `problem_solution_fit` is not `Cleared`. Do not write it yourself.
- D for "does not fit the strategy": judge against the active custom policy if one exists, otherwise against the user's stated goals and constraints.
- A `Refuted` risk that the canvas depends on usually means C (pivot) unless the canvas has already been revised around it.
- The rank never sets `status_decision`. The user may park an A or pursue a C; when they do, leave one line in `review_personal` explaining why.
- In `PostHoc` mode, omit `review_rank`. Do not turn past success into a present S.

## Points to Question (feed the grade and the risk rows)

Most questions belong to a risk row; write the observation there, not in a separate section.

- Customer: Are early adopters a true wedge (not too narrow to expand, not too broad to resonate)? In two-sided or ad models, do both the problem owner and the payer have incentives?
- Market: Is there a paid acquisition channel that scales beyond initial reach? Does the product disguise labor-intensive operations that get harder with headcount? If the unfair advantage is empty (normal early on), is it still claiming a massive market without a defensibility path?
- Product: Is it a real pain or a nice-to-have? Are alternatives merely "cumbersome, but working"?
- Overall: Is the map unified, or do boxes describe separate businesses?

Not in the canvas, but they shape the grade (do not fabricate; mark as "Undecided" / "未決" with rationale if unknown, and mention them in `reason` or `review_personal` only when they move the grade):

- Founder-market fit
- Why now (regulation, platforms, shifts in habit)
- Venture scale or independent business: is this suited to external capital returns, or sufficient as an independent business? Grade against the user's actual goal; do not downgrade a sound independent business for lacking venture scale.
