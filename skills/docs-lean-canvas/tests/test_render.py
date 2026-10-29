from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import render


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


class RenderTests(unittest.TestCase):
    def test_generated_tables_have_no_formatting_newlines(self):
        import re
        for lang in ['ja', 'en']:
            out = render.render_md({'review_personal': ['One', 'Two']}, lang=lang)
            tables = re.findall(r'<table\b.*?</table>', out, re.S)
            self.assertEqual(len(tables), 5)
            for table in tables:
                self.assertNotIn('\n', table)


    def test_risk_stage_fragile_and_rank_rows(self):
        data = {
            'meta': {'canvas_type': 'New'},
            'review_risks': {
                'customer': {'status': 'Signal', 'comment': 'No channel yet'},
                'market': {'status': 'Untested', 'comment': 'X is $12/mo'},
                'product': {'status': 'Supported', 'comment': '5 interviews'},
            },
            'review_stages': {
                'problem_solution_fit': {'status': 'InProgress', 'comment': 'Customer is Signal'},
                'product_market_fit': {'status': 'NotStarted', 'comment': 'After PSF'},
                'scale': {'status': 'NotStarted'},
            },
            'review_fragile_hypothesis': {'risk': 'customer', 'hypothesis': 'Users pay', 'experiment': 'Ask 5 users'},
            'review_rank': {'grade': 'A', 'reason': 'Reach is the weakest'},
            'review_personal': ['Pitfall note'],
        }
        cases = [
            ('ja', ['### メタ情報', '種別', '### リスク', '顧客', '[兆候あり] No channel yet', '市場', '[未検証] X is $12/mo',
                    'プロダクト（課題・解決策）', '[裏付けあり] 5 interviews',
                    '### 検証', '課題／解決策フィット', '[検証中] Customer is Signal', '製品／市場フィット', '[未着手] After PSF',
                    '拡大', '脆い仮説', '軸: 顧客', '仮説: Users pay', '検証: Ask 5 users',
                    '### 総評', 'ランク', 'A（見込み・未検証）', '一言', 'Reach is the weakest', '所見', 'Pitfall note']),
            ('en', ['### Meta', 'Type', '### Risks', 'Customer', '[Signal] No channel yet', 'Market', '[Untested] X is $12/mo',
                    'Product (Problem / Solution)', '[Supported] 5 interviews',
                    '### Validation', 'Problem / Solution Fit', '[In progress] Customer is Signal', 'Product / Market Fit',
                    '[Not started] After PSF', 'Scale', 'Fragile Hypothesis', 'Axis: Customer',
                    'Hypothesis: Users pay', 'Experiment: Ask 5 users',
                    '### Overall Review', 'Rank', 'A (prospect, unverified)', 'Reason', 'Reach is the weakest',
                    'Notes', 'Pitfall note']),
        ]
        for lang, labels in cases:
            with self.subTest(lang=lang):
                out = render.render_md(data, lang=lang)
                out = out[out.index('### '):]
                positions = [out.index(label) for label in labels]
                self.assertEqual(positions, sorted(positions))
                self.assertNotIn('Investor', out)
                self.assertNotIn('投資家', out)

    def test_rank_is_not_marked_unverified_once_problem_solution_fit_is_cleared(self):
        for grade, stage, marked in [('A', 'Cleared', False), ('S', 'InProgress', True), ('B', 'InProgress', False)]:
            with self.subTest(grade=grade, stage=stage):
                out = render.render_md({'review_rank': {'grade': grade},
                                        'review_stages': {'problem_solution_fit': {'status': stage}}}, lang='en')
                self.assertIn(f'>{grade}', out)
                self.assertEqual('(prospect, unverified)' in out, marked)

    def test_cleared_stage_without_supported_risks_warns(self):
        data = {
            'review_risks': {'customer': {'status': 'Supported'}, 'product': {'status': 'Signal'},
                             'market': {'status': 'Supported'}},
            'review_stages': {'problem_solution_fit': {'status': 'Cleared'},
                              'scale': {'status': 'Cleared'}},
        }
        warnings = render.validation_warnings(data)
        self.assertTrue(any('problem_solution_fit' in w and 'product' in w for w in warnings), warnings)
        self.assertTrue(any('scale' in w and 'product_market_fit' in w for w in warnings), warnings)
        data['review_risks']['product']['status'] = 'Supported'
        data['review_stages'].pop('scale')
        self.assertEqual(render.validation_warnings(data), [])
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'warn.lean-canvas.yaml'
            src.write_text('review_risks:\n  customer:\n    status: Untested\nreview_stages:\n'
                           '  problem_solution_fit:\n    status: Cleared\n', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/render.py'), str(src)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('warning: problem_solution_fit is Cleared', result.stderr)
            self.assertTrue(src.with_suffix('.md').exists())

    def test_legacy_problem_and_investor_reviews_are_still_shown(self):
        data = {'review_problem': ['Competitor: X - $10/mo'], 'review_investor': ['Too small for VC'],
                'review_personal': ['Note']}
        out = render.render_md(data, lang='ja')
        self.assertIn('課題調査: Competitor: X - $10/mo', out)
        self.assertLess(out.index('プロダクト（課題・解決策）'), out.index('課題調査: '))
        self.assertLess(out.index('Note'), out.index('投資家視点: Too small for VC'))

    def test_new_canvas_keeps_empty_rows_but_posthoc_drops_them(self):
        new = render.render_md({'meta': {'canvas_type': 'New'}}, lang='en')
        for label in ['### Risks', '### Validation', 'Stage: ', 'Fragile Hypothesis', '>Rank<', '>Reason<']:
            self.assertEqual(label in new, label != 'Stage: ', label)
        posthoc = render.render_md({'meta': {'canvas_type': 'PostHoc'}, 'review_personal': ['Note'],
                                    'review_risks': {'market': {'status': 'Signal', 'comment': 'Ads'}}}, lang='en')
        for label in ['>Customer<', '>Product (Problem', '### Validation', 'Fragile Hypothesis', '>Reason<']:
            self.assertNotIn(label, posthoc)
        for label in ['### Meta', '### Risks', '[Signal] Ads', '### Overall Review', '>Rank<',
                      '- (not ranked for post-hoc)', '>Notes<']:
            self.assertIn(label, posthoc)

    def test_cascade_specificity_source_order_inline_and_important(self):
        text = '<div class="outer"><b class="item" style="color: black; padding: 9px !important; margin: 4px">x</b></div>'
        css = '''.outer .item { color: red; margin-top: 2px; }
                 b { color: blue; margin: 0; }
                 .item { color: green !important; padding: 3px !important; }
                 b { color: orange !important; }
                 .item { color: purple !important; }'''
        result = render.inline_css(text, css)
        style = Elements(result).nodes[1][1]['style']
        self.assertLess(style.index('color: blue;'), style.index('color: red;'))
        self.assertLess(style.index('color: red;'), style.index('color: black;'))
        self.assertLess(style.index('color: black;'), style.index('color: orange !important;'))
        self.assertLess(style.index('color: orange !important;'), style.index('color: green !important;'))
        self.assertLess(style.index('color: green !important;'), style.index('color: purple !important;'))
        self.assertLess(style.index('padding: 3px !important;'), style.index('padding: 9px !important;'))
        self.assertLess(style.index('margin: 0;'), style.index('margin-top: 2px;'))
        self.assertLess(style.index('margin-top: 2px;'), style.index('margin: 4px;'))

    def test_descendants_first_last_child_and_entity_preservation(self):
        text = '# 日本語 &amp; English\n<table class="review"><tr>\n<!-- ignore -->\n<td><b>&lt;x&gt;</b></td><td>last</td></tr></table>\n'
        css = '.review td:first-child { width: 7.5em; } .review td:last-child { padding: 8px; } .review b { color: red; }'
        out = render.inline_css(text, css)
        nodes = Elements(out).nodes
        self.assertIn('width: 7.5em', nodes[2][1]['style'])
        self.assertNotIn('padding', nodes[2][1]['style'])
        self.assertIn('padding: 8px', nodes[4][1]['style'])
        self.assertNotIn('width', nodes[4][1]['style'])
        self.assertIn('color: red', nodes[3][1]['style'])
        self.assertTrue(out.startswith('# 日本語 &amp; English\n'))
        self.assertIn('&lt;x&gt;', out)
        self.assertNotIn('&amp;lt;', out)

    def test_cli_language_override_custom_css_and_legacy_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dest, css = (Path(tmp) / name for name in ['source.yaml', 'out.md', 'source.css'])
            src.write_text('meta:\n  lang: ja\n', encoding='utf-8')
            css.write_text('.lc { color: red; }', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/render.py'), str(src), str(dest),
                                     '--lang', 'en', '--css-src', str(css), '--css-href', 'ignored.css',
                                     '--no-copy-css'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            out = dest.read_text()
            self.assertIn('Problem', out)
            self.assertNotIn('課題', out)
            self.assertNotIn('ignored.css', out)
            self.assertIn('color: red', out)

    def test_invalid_templates_are_rejected(self):
        for text in ['<style>td { color:red; }</style>', '<link href="x">', '<table><td></table>', '<div>']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                render.inline_css(text, '')

    def test_reject_unsupported_css_before_overwriting_output(self):
        for css in ['td:hover { color: red; }', '@media print { td { color: red; } }',
                    'td > b { color: red; }', 'td { color red; }',
                    'td { color: var(--ink); }', 'td { unknown-property: red; }']:
            with self.subTest(css=css), tempfile.TemporaryDirectory() as tmp:
                src = Path(tmp) / 'canvas.yaml'
                dest = src.with_suffix('.md')
                style = Path(tmp) / 'custom.css'
                src.write_text('meta:\n  lang: ja\n', encoding='utf-8')
                dest.write_text('KEEP', encoding='utf-8')
                style.write_text(css, encoding='utf-8')
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/render.py'),
                                         str(src), '--css-src', str(style)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('unsupported CSS', result.stderr)
                self.assertEqual(dest.read_text(), 'KEEP')

    def test_self_contained_bilingual_cli(self):
        for lang, label in [('ja', '課題'), ('en', 'Problem')]:
            with self.subTest(lang=lang), tempfile.TemporaryDirectory() as tmp:
                src = Path(tmp) / 'example.lean-canvas.yaml'
                src.write_text('meta:\n  project_name: "Test <&>"\n  lang: ' + lang + '\ncanvas:\n  problem:\n    top_3_problems:\n      - "<script>alert(1)</script> & text"\n', encoding='utf-8')
                original = src.read_bytes()
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/render.py'), str(src)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                out = src.with_suffix('.md').read_text(encoding='utf-8')
                self.assertNotRegex(out, r'<(?:link|style)\b|\bclass=')
                self.assertFalse((Path(tmp) / 'lean-canvas.css').exists())
                self.assertEqual(src.read_bytes(), original)
                self.assertIn(label, out)
                self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt; &amp; text', out)
                nodes = Elements(out).nodes
                tables = [a for t, a in nodes if t == 'table']
                self.assertEqual(len(tables), 5)
                self.assertIn('table-layout: fixed !important', tables[0]['style'])
                self.assertIn('background: #ffffff', tables[0]['style'])
                cells = [a for t, a in nodes if t == 'td']
                self.assertEqual([a.get('colspan') for a in cells[:5]], ['2'] * 5)
                self.assertEqual(sum(a.get('rowspan') == '2' for a in cells), 3)
                self.assertIn('background: #f7edea', cells[0]['style'])
                self.assertIn('color: #272a2e', cells[0]['style'])
                self.assertIn('width: 7.5em', cells[9]['style'])
                self.assertIn('padding: 8px !important', cells[10]['style'])
                self.assertTrue(any(t == 'div' and 'background: #ead4cf' in a.get('style', '') for t, a in nodes))
                self.assertTrue(any(t == 'ul' and 'margin-top: 0.25em' in a.get('style', '') for t, a in nodes))


if __name__ == '__main__':
    unittest.main()
