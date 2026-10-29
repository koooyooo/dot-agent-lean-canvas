#!/usr/bin/env python3
"""YAML の Lean Canvas から Markdown（HTML 表）を出す。依存なし。
表は assets/template.md (または assets/template_en.md)、見た目は assets/lean-canvas.css。
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

from inline_css import inline_css


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS_CSS = SKILL_ROOT / "assets" / "lean-canvas.css"
TEMPLATE_MD = SKILL_ROOT / "assets" / "template.md"
TEMPLATE_EN_MD = SKILL_ROOT / "assets" / "template_en.md"
TOKEN = re.compile(r"\{\{[a-z_]+\}\}")
RISKS = ("customer", "market", "product")
STAGES = ("problem_solution_fit", "product_market_fit", "scale")
# A stage may be Cleared only when these risks are Supported and the previous stage is Cleared.
STAGE_REQUIRES = {
    "problem_solution_fit": (("customer", "product"), None),
    "product_market_fit": (("market", "product"), "problem_solution_fit"),
    "scale": (("market",), "product_market_fit"),
}

I18N = {
    "ja": {
        "blurb_posthoc": "既存サービスの後追いサンプル。公式資料ではない。",
        "blurb_new": (
            "表は公式 Lean Canvas の 5 列（課題・顧客が左右端、UVP が中央）。"
            "メタ情報・リスク・検証・総評は下の 4 つの表。"
            "装飾は各要素の style 属性に展開する。表はネストしない。プレースホルダは残さない。"
        ),
        "undecided": "未決",
        "concept_prefix": "例え: ",
        "acquisition_prefix": "獲得: ",
        "activation_prefix": "活性化: ",
        "retention_prefix": "継続: ",
        "fixed_prefix": "固定",
        "variable_prefix": "変動",
        "monetization_prefix": "課金: ",
        "pricing_prefix": "価格: ",
        "ltv_prefix": "LTV: ",
        "hypothesis_prefix": "仮説: ",
        "experiment_prefix": "検証: ",
        "risk_axis_prefix": "軸: ",
        "rank_unverified": "（見込み・未検証）",
        "rank_posthoc": "-（後追いのため付けない）",
        "legacy_problem_prefix": "課題調査: ",
        "legacy_investor_prefix": "投資家視点: ",
        "risk_status": {"Untested": "未検証", "Signal": "兆候あり", "Supported": "裏付けあり", "Refuted": "否定"},
        "stage_status": {"NotStarted": "未着手", "InProgress": "検証中", "Cleared": "クリア"},
        "risk_names": {"customer": "顧客", "market": "市場", "product": "プロダクト"},
    },
    "en": {
        "blurb_posthoc": "Post-hoc retrospective sample of an existing service. Not an official document.",
        "blurb_new": (
            "Standard 5-column Lean Canvas (Problem and Customer at edges, UVP in center). "
            "Meta, Risks, Validation, and Overall Review are in the four tables below. "
            "Styles are inline on each element. Tables are not nested. No unfilled placeholders."
        ),
        "undecided": "Undecided",
        "concept_prefix": "Concept: ",
        "acquisition_prefix": "Acquisition: ",
        "activation_prefix": "Activation: ",
        "retention_prefix": "Retention: ",
        "fixed_prefix": "Fixed",
        "variable_prefix": "Variable",
        "monetization_prefix": "Model: ",
        "pricing_prefix": "Pricing: ",
        "ltv_prefix": "LTV: ",
        "hypothesis_prefix": "Hypothesis: ",
        "experiment_prefix": "Experiment: ",
        "risk_axis_prefix": "Axis: ",
        "rank_unverified": " (prospect, unverified)",
        "rank_posthoc": "- (not ranked for post-hoc)",
        "legacy_problem_prefix": "Problem research: ",
        "legacy_investor_prefix": "Investor view: ",
        "risk_status": {"Untested": "Untested", "Signal": "Signal", "Supported": "Supported", "Refuted": "Refuted"},
        "stage_status": {"NotStarted": "Not started", "InProgress": "In progress", "Cleared": "Cleared"},
        "risk_names": {"customer": "Customer", "market": "Market", "product": "Product"},
    },
}


class YamlError(Exception):
    pass


def _parse_quoted(s: str, quote: str) -> tuple[str, str]:
    i = 1
    out = []
    while i < len(s):
        c = s[i]
        if quote == '"' and c == "\\":
            if i + 1 >= len(s):
                raise YamlError("unterminated escape")
            nxt = s[i + 1]
            out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\", "'": "'"}.get(nxt, nxt))
            i += 2
            continue
        if quote == "'" and c == "'" and i + 1 < len(s) and s[i + 1] == "'":
            out.append("'")
            i += 2
            continue
        if c == quote:
            return "".join(out), s[i + 1 :].lstrip()
        out.append(c)
        i += 1
    raise YamlError("unterminated string")


def _parse_scalar(raw: str) -> str:
    s = raw.strip()
    if not s:
        return ""
    if s[0] in "\"'":
        val, rest = _parse_quoted(s, s[0])
        if rest.startswith("#"):
            rest = ""
        if rest:
            raise YamlError(f"trailing junk after string: {rest!r}")
        return val
    if " #" in s:
        s = s.split(" #", 1)[0].rstrip()
    return s


def _tokenize(text: str) -> list[tuple[int, str, int]]:
    tokens = []
    for n, line in enumerate(text.splitlines(), 1):
        if "\t" in line:
            raise YamlError(f"line {n}: tabs are not allowed")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        tokens.append((indent, line.strip(), n))
    return tokens


def _parse_block(tokens: list[tuple[int, str, int]], i: int, indent: int):
    if i >= len(tokens):
        return None, i
    ind, content, n = tokens[i]
    if ind < indent:
        return None, i
    if content.startswith("- "):
        return _parse_seq(tokens, i, indent)
    return _parse_map(tokens, i, indent)


def _split_key(content: str, n: int) -> tuple[str, str | None]:
    if content.startswith("- "):
        raise YamlError(f"line {n}: expected mapping")
    in_q = None
    for i, c in enumerate(content):
        if in_q:
            if c == "\\" and in_q == '"':
                continue
            if c == in_q:
                in_q = None
            continue
        if c in "\"'":
            in_q = c
            continue
        if c == ":" and (i + 1 == len(content) or content[i + 1] in " #"):
            key = content[:i].strip()
            rest = content[i + 1 :].strip()
            if rest.startswith("#"):
                rest = ""
            return key, rest if rest else None
        if c == ":":
            key = content[:i].strip()
            rest = content[i + 1 :].strip()
            if rest.startswith("#"):
                rest = ""
            return key, rest if rest else None
    raise YamlError(f"line {n}: missing ':'")


def _parse_map(tokens, i, indent) -> tuple[dict, int]:
    out = {}
    while i < len(tokens):
        ind, content, n = tokens[i]
        if ind < indent:
            break
        if ind > indent:
            raise YamlError(f"line {n}: bad indent")
        if content.startswith("- "):
            raise YamlError(f"line {n}: sequence in mapping")
        key, inline = _split_key(content, n)
        i += 1
        if inline is not None:
            out[key] = _parse_scalar(inline)
            continue
        if i >= len(tokens) or tokens[i][0] <= indent:
            out[key] = {}
            continue
        child_indent = tokens[i][0]
        if child_indent <= indent:
            out[key] = {}
            continue
        val, i = _parse_block(tokens, i, child_indent)
        out[key] = val
    return out, i


def _parse_seq(tokens, i, indent) -> tuple[list, int]:
    out = []
    while i < len(tokens):
        ind, content, n = tokens[i]
        if ind < indent:
            break
        if ind > indent:
            raise YamlError(f"line {n}: bad indent")
        if not content.startswith("- "):
            break
        rest = content[2:].strip()
        i += 1
        if not rest:
            if i < len(tokens) and tokens[i][0] > indent:
                val, i = _parse_block(tokens, i, tokens[i][0])
                out.append(val)
            else:
                out.append("")
            continue
        out.append(_parse_scalar(rest))
        if i < len(tokens) and tokens[i][0] > indent:
            raise YamlError(f"line {tokens[i][2]}: nested value under scalar list item")
    return out, i


def loads(text: str) -> dict:
    tokens = _tokenize(text)
    if not tokens:
        return {}
    val, i = _parse_block(tokens, 0, tokens[0][0])
    if i != len(tokens):
        raise YamlError(f"line {tokens[i][2]}: leftover")
    if not isinstance(val, dict):
        raise YamlError("root must be a mapping")
    return val


def _as_list(val) -> list[str]:
    if val is None or val == {} or val == []:
        return []
    if isinstance(val, list):
        out = []
        for x in val:
            if isinstance(x, dict):
                out.append(", ".join(f"{k}: {v}" for k, v in x.items()))
            else:
                out.append(str(x))
        return out
    return [str(val)]


def _li(text: str) -> str:
    return f"<li>{html.escape(text)}</li>"


def _lis(items: list[str], empty: str = "未決") -> str:
    rows = items if items else [empty]
    return "\n          ".join(_li(x) for x in rows)


def _prefixed_items(prefix: str, val, empty: str = "未決") -> list[str]:
    items = _as_list(val)
    if not items:
        return [f"{prefix}: {empty}"]
    return [f"{prefix}: {x}" for x in items]


def _review_cell(items: list[str]) -> str:
    if not items:
        return ""
    inner = "\n        ".join(_li(x) for x in items)
    return f"\n      <ul>\n        {inner}\n      </ul>\n    "


def _fragile_items(val, i18n: dict) -> list[str]:
    if not isinstance(val, dict):
        return _as_list(val)
    items = []
    if val.get("risk"):
        risk = str(val["risk"])
        items.append(f"{i18n['risk_axis_prefix']}{i18n['risk_names'].get(risk, risk)}")
    if val.get("hypothesis"):
        items.append(f"{i18n['hypothesis_prefix']}{val['hypothesis']}")
    if val.get("experiment"):
        items.append(f"{i18n['experiment_prefix']}{val['experiment']}")
    return items


def _status(val) -> str:
    return str(val.get("status") or "") if isinstance(val, dict) else ""


def _status_items(val, labels: dict) -> list[str]:
    """{status, comment} -> one line such as "[兆候あり] comment"."""
    if not isinstance(val, dict):
        return _as_list(val)
    status = _status(val)
    comment = str(val.get("comment") or "")
    label = f"[{labels.get(status, status)}]" if status else ""
    line = " ".join(x for x in (label, comment) if x)
    return [line] if line else []


def _rank_grade(val, stages: dict, i18n: dict) -> str:
    if not isinstance(val, dict) or not val.get("grade"):
        return ""
    grade = str(val["grade"]).strip()
    # S/A is a prospect until problem/solution fit is cleared; say so in the cell.
    if grade in ("S", "A") and stages and _status(stages.get("problem_solution_fit")) != "Cleared":
        grade += i18n["rank_unverified"]
    return html.escape(grade)


def _rank_reason(val) -> list[str]:
    if isinstance(val, dict):
        return _as_list(val.get("reason"))
    return _as_list(val)


def validation_warnings(data: dict) -> list[str]:
    """Stages marked Cleared without the risks or previous stage they depend on."""
    risks = data.get("review_risks") or {}
    stages = data.get("review_stages") or {}
    if not isinstance(risks, dict) or not isinstance(stages, dict):
        return []
    out = []
    for stage, (needed, previous) in STAGE_REQUIRES.items():
        if _status(stages.get(stage)) != "Cleared":
            continue
        missing = [r for r in needed if _status(risks.get(r)) != "Supported"]
        if missing:
            out.append(f"{stage} is Cleared but risks are not Supported: {', '.join(missing)}")
        if previous and _status(stages.get(previous)) != "Cleared":
            out.append(f"{stage} is Cleared but {previous} is not Cleared")
    return out


def _drop_empty_rows(template: str, keys: list[str]) -> str:
    for key in keys:
        template = re.sub(r"[ \t]*<tr>\s*<td>[^<]*</td>\s*<td>\{\{" + key + r"\}\}</td>\s*</tr>\n?", "", template)
    # A table left without rows goes away together with its heading.
    return re.sub(r"### [^\n]*\n\s*<table\b[^>]*>\s*</table>\n?\n?", "", template)


def _fill(template: str, values: dict[str, str]) -> str:
    out = template
    for key, val in values.items():
        out = out.replace("{{" + key + "}}", val)
    leftover = TOKEN.findall(out)
    if leftover:
        raise SystemExit("unfilled placeholders: " + ", ".join(sorted(set(leftover))))
    return out


def _resolve_lang(explicit_lang: str | None, meta: dict) -> str:
    if explicit_lang:
        return explicit_lang.lower()
    val = meta.get("lang") or meta.get("language")
    if val:
        return str(val).strip().lower()
    return "ja"


def render_md(data: dict, css_href: str = "lean-canvas.css", template_path: Path | None = None, lang: str | None = None, css_src: Path = ASSETS_CSS) -> str:
    # css_href is retained for callers of the old API; output is always inline.
    meta = data.get("meta") or {}
    canvas = data.get("canvas") or {}
    resolved_lang = _resolve_lang(lang, meta)
    if resolved_lang not in I18N:
        resolved_lang = "ja"
    i18n = I18N[resolved_lang]

    if template_path is None:
        template_path = TEMPLATE_EN_MD if resolved_lang == "en" else TEMPLATE_MD

    if not template_path.is_file():
        raise SystemExit(f"missing {template_path}")
    raw = re.sub(r"<!--.*?-->\s*", "", template_path.read_text(encoding="utf-8"), count=1, flags=re.S)

    canvas_type = str(meta.get("canvas_type") or "-")
    if canvas_type == "PostHoc":
        blurb = i18n["blurb_posthoc"]
    else:
        blurb = i18n["blurb_new"]

    problem = canvas.get("problem") or {}
    solution = canvas.get("solution") or {}
    uvp = canvas.get("unique_value_proposition") or {}
    unfair = canvas.get("unfair_advantage") or {}
    customer = canvas.get("customer_segments") or {}
    metrics = canvas.get("key_metrics") or {}
    channels = canvas.get("channels") or {}
    cost = canvas.get("cost_structure") or {}
    revenue = canvas.get("revenue_streams") or {}
    risks = data.get("review_risks") if isinstance(data.get("review_risks"), dict) else {}
    stages = data.get("review_stages") if isinstance(data.get("review_stages"), dict) else {}
    default_empty = i18n["undecided"]
    headline = str(uvp.get("headline") or default_empty)
    concept = str(uvp.get("high_level_concept") or default_empty)

    values = {
        "project_name": html.escape(str(meta.get("project_name") or default_empty)),
        "blurb": blurb,
        "css_href": html.escape(css_href),
        "lis_problems": _lis(_as_list(problem.get("top_3_problems")), empty=default_empty),
        "lis_alternatives": _lis(_as_list(problem.get("existing_alternatives")), empty=default_empty),
        "lis_features": _lis(_as_list(solution.get("top_3_features")), empty=default_empty),
        "lis_uvp": _lis([headline, f"{i18n['concept_prefix']}{concept}"], empty=default_empty),
        "lis_unfair": _lis(_as_list(unfair.get("defensibility")), empty=default_empty),
        "lis_customers": _lis(_as_list(customer.get("target_customers")), empty=default_empty),
        "lis_early": _lis(_as_list(customer.get("early_adopters")), empty=default_empty),
        "lis_metrics": _lis([
            f"{i18n['acquisition_prefix']}{metrics.get('acquisition') or default_empty}",
            f"{i18n['activation_prefix']}{metrics.get('activation') or default_empty}",
            f"{i18n['retention_prefix']}{metrics.get('retention') or default_empty}",
        ], empty=default_empty),
        "lis_channels": _lis(_as_list(channels.get("inbound_and_outbound")), empty=default_empty),
        "lis_cost": _lis(
            _prefixed_items(i18n["fixed_prefix"], cost.get("fixed_costs"), empty=default_empty)
            + _prefixed_items(i18n["variable_prefix"], cost.get("variable_costs"), empty=default_empty),
            empty=default_empty,
        ),
        "lis_revenue": _lis([
            f"{i18n['monetization_prefix']}{revenue.get('monetization_model') or default_empty}",
            f"{i18n['pricing_prefix']}{revenue.get('pricing') or default_empty}",
            f"{i18n['ltv_prefix']}{revenue.get('lifetime_value_estimate') or default_empty}",
        ], empty=default_empty),
        "canvas_type": html.escape(canvas_type),
        "status_canvas": html.escape(str(meta.get("status_canvas") or "-")),
        "status_decision": html.escape(str(meta.get("status_decision") or "-")),
        "cell_review_fragile": _review_cell(_fragile_items(data.get("review_fragile_hypothesis"), i18n)),
        "cell_rank_grade": _rank_grade(data.get("review_rank"), stages, i18n),
        "cell_rank_reason": _review_cell(_rank_reason(data.get("review_rank"))),
        "cell_review_personal": _review_cell(
            _as_list(data.get("review_personal"))
            + [i18n["legacy_investor_prefix"] + x for x in _as_list(data.get("review_investor"))]
        ),
    }
    for risk in RISKS:
        items = _status_items(risks.get(risk), i18n["risk_status"])
        if risk == "product":
            # Older canvases kept market research in review_problem.
            items += [i18n["legacy_problem_prefix"] + x for x in _as_list(data.get("review_problem"))]
        values[f"cell_risk_{risk}"] = _review_cell(items)
    for stage in STAGES:
        values[f"cell_stage_{stage}"] = _review_cell(_status_items(stages.get(stage), i18n["stage_status"]))

    optional = [k for k in values if k.startswith(("cell_risk_", "cell_stage_", "cell_rank_")) or k == "cell_review_fragile"]
    if canvas_type == "PostHoc":
        # Case studies are not bets; say why the rank is missing, and leave out validation rows they did not fill.
        values["cell_rank_grade"] = values["cell_rank_grade"] or html.escape(i18n["rank_posthoc"])
        raw = _drop_empty_rows(raw, [k for k in optional if not values[k]])
    for key in optional:
        values[key] = values[key] or "-"
    rendered = inline_css(_fill(raw, values), css_src.read_text(encoding="utf-8"))
    # Obsidian / Markdown renderers treat intra-tag newlines inside <table> as line breaks (<br>)
    # or blank lines, creating a gap above cell headers. Strip whitespace between tags inside tables.
    def clean_table(m):
        return re.sub(r'>\s*\n\s*<', '><', m.group(0))
    return re.sub(r'<table\b.*?</table>', clean_table, rendered, flags=re.DOTALL)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Render Lean Canvas YAML to Markdown HTML tables")
    p.add_argument("yaml_path", type=Path)
    p.add_argument("md_path", nargs="?", type=Path)
    p.add_argument("--lang", choices=["ja", "en"], default=None, help="Language (ja or en). Default inferred from YAML or 'ja'")
    p.add_argument("--css-href", default="lean-canvas.css", help="Deprecated; ignored (styles are inline)")
    p.add_argument("--css-src", type=Path, default=ASSETS_CSS)
    p.add_argument("--template", type=Path, default=None)
    p.add_argument("--no-copy-css", action="store_true", help="Deprecated; CSS is never copied")
    args = p.parse_args(argv)

    src = args.yaml_path
    if not src.is_file():
        print(f"not found: {src}", file=sys.stderr)
        return 1
    try:
        data = loads(src.read_text(encoding="utf-8"))
    except YamlError as e:
        print(f"yaml: {e}", file=sys.stderr)
        return 1

    md_path = args.md_path
    if md_path is None:
        md_path = src.with_suffix(".md")
        if src.suffix == ".yaml" and src.name.endswith(".lean-canvas.yaml"):
            md_path = src.with_name(src.name[: -len(".yaml")] + ".md")

    try:
        text = render_md(data, args.css_href, args.template, args.lang, args.css_src)
    except (ValueError, OSError) as e:
        print(f"render: {e}", file=sys.stderr)
        return 1
    for warning in validation_warnings(data):
        print(f"warning: {warning}", file=sys.stderr)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
