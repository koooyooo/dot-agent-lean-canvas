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

I18N = {
    "ja": {
        "blurb_posthoc": "既存サービスの後追いサンプル。公式資料ではない。",
        "blurb_new": (
            "表は公式 Lean Canvas の 5 列（課題・顧客が左右端、UVP が中央）。"
            "種別・キャンバス完成・決定・レビュー・投資家視点は下の表。"
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
    },
    "en": {
        "blurb_posthoc": "Post-hoc retrospective sample of an existing service. Not an official document.",
        "blurb_new": (
            "Standard 5-column Lean Canvas (Problem and Customer at edges, UVP in center). "
            "Type, Canvas Status, Decision, Review, and Investor View are in the table below. "
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
        "cell_review_personal": _review_cell(_as_list(data.get("review_personal"))),
        "cell_review_investor": _review_cell(_as_list(data.get("review_investor"))),
    }
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
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
