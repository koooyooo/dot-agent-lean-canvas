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
            self.assertEqual(len(tables), 2)
            for table in tables:
                self.assertNotIn('\n', table)


    def test_problem_and_fragile_hypothesis_review_rows(self):
        data = {
            'review_problem': ['Competitor: X - $10/mo'],
            'review_fragile_hypothesis': {'hypothesis': 'Users pay', 'experiment': 'Ask 5 users'},
        }
        for lang, labels in [('ja', ['レビュー: 課題', 'レビュー: 総評', 'レビュー: 脆い仮説', '仮説: Users pay', '検証: Ask 5 users']),
                             ('en', ['Review: Problem', 'Review: Overall', 'Review: Fragile Hypothesis', 'Hypothesis: Users pay', 'Experiment: Ask 5 users'])]:
            out = render.render_md(data, lang=lang)
            for label in labels + ['Competitor: X - $10/mo']:
                self.assertIn(label, out)
            self.assertLess(out.index(labels[0]), out.index(labels[1]))
            self.assertLess(out.index(labels[1]), out.index(labels[2]))

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
                self.assertEqual(len(tables), 2)
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
