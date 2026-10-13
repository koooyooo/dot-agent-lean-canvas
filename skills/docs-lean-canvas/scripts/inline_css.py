"""Inline the canvas CSS subset using only the standard library.

Supports tag/class compounds, descendants, selector lists and first/last-child.
Rejects unsupported syntax. Not a general CSS or HTML engine; templates must
have explicit, balanced end tags (except HTML void elements).
"""
from html import escape
from html.parser import HTMLParser
import re


PART = re.compile(r'(?P<tag>[a-z][a-z0-9-]*)?(?P<classes>(?:\.[a-zA-Z_][\w-]*)*)(?P<pseudo>:(?:first|last)-child)?\Z')
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
# Intentionally limited to the canvas authoring vocabulary, not arbitrary CSS.
PROPERTIES = set('''display width max-width min-width table-layout overflow
    border-collapse margin margin-top margin-right margin-bottom margin-left
    padding padding-top padding-right padding-bottom padding-left font-family
    font-size font-weight line-height color background box-sizing border
    border-top border-bottom vertical-align overflow-wrap word-break white-space'''.split())


def declarations(text):
    result = []
    for declaration in text.split(';'):
        if not declaration.strip():
            continue
        match = re.fullmatch(r'\s*([a-z][a-z-]*)\s*:\s*([#\w.,%\s-]+?)(\s*!important)?\s*', declaration)
        if not match:
            raise ValueError(f'unsupported CSS declaration: {declaration!r}')
        prop, value, important = match.groups()
        if prop not in PROPERTIES:
            raise ValueError(f'unsupported CSS property: {prop!r}')
        result.append((prop, value.strip(), bool(important)))
    return result


def rules(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    result = []
    while css.strip():
        match = re.match(r'\s*([^{}]+)\{([^{}]*)\}', css)
        if not match:
            raise ValueError('unsupported CSS rule: ' + css[:80])
        selectors, body = match.groups()
        decls = declarations(body)
        for selector in selectors.split(','):
            parts = []
            for token in selector.split():
                part = PART.fullmatch(token)
                if not part or not any(part.groups()):
                    raise ValueError(f'unsupported CSS selector: {selector!r}')
                tag, classes, pseudo = part.groups()
                parts.append((tag, classes.split('.')[1:], pseudo))
            if not parts:
                raise ValueError('empty CSS selector')
            specificity = (0, sum(len(c) + bool(p) for _, c, p in parts), sum(bool(t) for t, _, _ in parts))
            result.append((parts, specificity, decls))
        css = css[match.end():]
    return result


class Node:
    def __init__(self, tag, attrs, parent, start, end, closed=False):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.start, self.end, self.closed = start, end, closed
        self.children = []
        if parent is not None:
            parent.children.append(self)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.offsets = [0]
        for line in text.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.nodes, self.stack = [], []
        self.feed(text)
        self.close()
        if self.stack:
            raise ValueError('unclosed HTML template tag')

    def handle_starttag(self, tag, attrs):
        self.add(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self.add(tag, attrs, True)

    def add(self, tag, attrs, closed):
        if tag in {'style', 'link'}:
            raise ValueError('inline templates must not contain style/link tags')
        line, column = self.getpos()
        start = self.offsets[line - 1] + column
        raw_tag = self.get_starttag_text()
        assert raw_tag is not None
        node = Node(tag, attrs, self.stack[-1] if self.stack else None,
                    start, start + len(raw_tag), closed)
        self.nodes.append(node)
        if tag not in VOID and not closed:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1].tag != tag:
            raise ValueError(f'unbalanced HTML template tag: {tag}')
        self.stack.pop()


def matches_part(node, part):
    tag, classes, pseudo = part
    if tag and node.tag != tag:
        return False
    if not set(classes).issubset(node.attrs.get('class', '').split()):
        return False
    if pseudo:
        if node.parent is None:
            return False
        sibling = node.parent.children[0 if pseudo == ':first-child' else -1]
        if node is not sibling:
            return False
    return True


def matches(node, parts):
    if not matches_part(node, parts[-1]):
        return False
    ancestor = node.parent
    for part in reversed(parts[:-1]):
        while ancestor is not None and not matches_part(ancestor, part):
            ancestor = ancestor.parent
        if ancestor is None:
            return False
        ancestor = ancestor.parent
    return True


def inline_css(text, css):
    stylesheet = rules(css)
    document = Document(text)
    replacements = []
    for node in document.nodes:
        cascade = []
        for parts, specificity, decls in stylesheet:
            if matches(node, parts):
                cascade.extend((important, specificity, prop, value) for prop, value, important in decls)
        cascade.extend((important, (1, 0, 0), prop, value)
                       for prop, value, important in declarations(node.attrs.get('style', '')))
        # Stable sorting preserves source order. Keep declarations, including
        # shorthands: browser evaluation then preserves margin/padding cascade.
        cascade.sort(key=lambda item: item[:2])
        style = '; '.join(f'{prop}: {value}' + (' !important' if important else '')
                          for important, _, prop, value in cascade)
        attrs = [(k, v) for k, v in node.attrs.items() if k not in {'class', 'style'}]
        if style:
            attrs.append(('style', style + ';'))
        rendered = '<' + node.tag + ''.join(
            f' {k}' if v is None else f' {k}="{escape(v, quote=True)}"' for k, v in attrs)
        rendered += ' />' if node.closed else '>'
        replacements.append((node.start, node.end, rendered))
    for start, end, replacement in reversed(replacements):
        text = text[:start] + replacement + text[end:]
    return text
