"""Optional real-layout regression: pip install playwright; playwright install chromium.

Set LEAN_CANVAS_BROWSER_CHANNEL=chrome to use an installed Google Chrome.
The renderer itself and the other tests remain dependency-free.
"""
import os
from pathlib import Path
import sys
import unittest

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import render


@unittest.skipIf(sync_playwright is None, 'optional Playwright layout test; see module docstring')
class BrowserLayoutTests(unittest.TestCase):
    def test_editor_whitespace_and_alignment_do_not_move_headers_or_lists(self):
        data = {
            'canvas': {
                'problem': {'top_3_problems': ['First & <item>', 'Second item']},
                'solution': {'top_3_features': ['Long solution text. ' * 35, 'Next solution']},
            },
            'review_personal': ['Review one', 'Review two'],
        }
        with sync_playwright() as p:
            channel = os.environ.get('LEAN_CANVAS_BROWSER_CHANNEL')
            browser = p.chromium.launch(headless=True, **({'channel': channel} if channel else {}))
            page = browser.new_page(viewport={'width': 1400, 'height': 1000})
            for lang in ['ja', 'en']:
                md = render.render_md(data, lang=lang)
                tables = md[md.index('<table'):]
                baseline = None
                for whitespace, middle in [('normal', False), ('pre-wrap', False),
                                           ('pre-line', False), ('normal', True),
                                           ('pre-wrap', True), ('pre-line', True),
                                           ('children-pre-wrap', True)]: 
                    with self.subTest(lang=lang, whitespace=whitespace, middle=middle):
                        css = f'body {{white-space:{whitespace}}}'
                        # Adversarial child rule, NOT a claim about Obsidian's live DOM.
                        if whitespace == 'children-pre-wrap':
                            css = 'td, div, ul, li {white-space:pre-wrap}'
                        if middle:
                            css += 'td {vertical-align:middle !important}'
                        page.set_content('<!doctype html><style>' + css + '</style>' + tables)
                        metrics = page.evaluate('''() => {
                            const tables = [...document.querySelectorAll('table')];
                            const cells = [...tables[0].querySelectorAll('td')];
                            const gaps = [...document.querySelectorAll('ul')].flatMap(ul =>
                                [...ul.children].slice(1).map(li => li.getBoundingClientRect().top -
                                    li.previousElementSibling.getBoundingClientRect().bottom));
                            return {
                                heights: tables.map(t => t.getBoundingClientRect().height),
                                headers: cells.map(c => c.firstElementChild.getBoundingClientRect().top -
                                    c.getBoundingClientRect().top),
                                gaps,
                                text: tables.map(t => t.textContent),
                                columns: tables[0].rows[0].cells.length,
                                rowspans: cells.filter(c => c.rowSpan === 2).length
                            };
                        }''')
                        if baseline is None:
                            baseline = metrics
                        self.assertEqual(metrics['columns'], 5)
                        self.assertEqual(metrics['rowspans'], 3)
                        self.assertEqual(metrics['text'], baseline['text'])
                        for gap in metrics['headers']:
                            self.assertLessEqual(gap, 1, metrics)
                        for actual, expected in zip(metrics['gaps'], baseline['gaps']):
                            self.assertAlmostEqual(actual, expected, delta=0.1)
                        for actual, expected in zip(metrics['heights'], baseline['heights']):
                            self.assertAlmostEqual(actual, expected, delta=0.1)
            browser.close()


if __name__ == '__main__':
    unittest.main()
