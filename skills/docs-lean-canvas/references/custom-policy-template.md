# Custom Policy Template

Copy this file to `references/custom-policy-{name}.md` (for example, `references/custom-policy-default.md` or `references/custom-policy-solo.md`) to apply your own evaluation criteria when creating or reviewing a `New` Lean Canvas.

All `references/custom-policy-*.md` files except `custom-policy-template.md` are ignored by Git, so your private strategy, financial targets, and domain constraints remain local.

## How This File Is Used

- Evaluated alongside "Common Pitfalls" when writing `review_personal` for `New` canvases. Validation-experiment criteria (section 4 below) apply to `review_fragile_hypothesis`.
- Do not add custom checklist fields to the YAML schema; record only triggered observations and concrete recommendations in `review_personal` / `review_fragile_hypothesis`.
- Skip this policy in `PostHoc` mode (retrospective case studies).

## Example Criteria to Customize

### 1. Creator / Team Fit
- Does this problem align with our core strengths, domain interest, and long-term motivation?
- Is this a domain we still want to work on over a multi-year horizon?

### 2. Operational & Architecture Constraints
- Can this product be built and operated within our target operational model (e.g., solo/small team, NoOps/serverless, automated support)?
- Are variable costs (e.g., LLM API tokens, infrastructure, third-party APIs) healthy relative to the target pricing?

### 3. Initial Reach & Monetization Milestones
- Is there a concrete, low-friction path to the first 5-10 paying users without requiring an enterprise sales force or large ad budget?
- Does the pricing model support our target revenue stages (e.g., recurring subscription vs. one-off labor)?

### 4. Next Minimum Validation Experiment
- Which single assumption on this canvas is the most fragile right now?
- What is the smallest experiment (completable within a few hours to a week before full implementation) to validate or falsify that assumption with real user behavior?
