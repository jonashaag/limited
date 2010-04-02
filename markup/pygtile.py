"""
    limited.markup.pygtile
    ~~~~~~~~~~~~~~~~~~~~~~
    A textile version that uses pygments to highlight code
"""
import re
from textile import Textile
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
pygments_formatter = HtmlFormatter(linenos=True, cssclass='code')

def pygmentize(code, language=None):
    if language is None:
        lexer = guess_lexer(code)
    else:
        lexer = get_lexer_by_name(language, stripall=True, tabsize=4)
    return highlight(code, lexer, pygments_formatter)


class Pygtiler(Textile):
    def code(self, text):
        return Textile.code(self, self.doSpecial(text, '`', '`', self._inline_code_))

    def _inline_code_(self, match):
        before, text, after = match.groups()

        code = self.shelve('<code>%s</code>' % text)
        return ''.join((before, code, after or ''))

    def getRefs(self, *args):
        _text = Textile.getRefs(self, *args)

        for match in re.findall('(<codeblock>(.+?)</codeblock>)', _text, re.DOTALL):
            # get language if set
            match, text = match
            while text.startswith('\n'):
                text = text[1:]
            while text.endswith('\n'):
                text = text[:-1]
            lang = re.match('^\(([a-z]+)\)', text)
            if lang is not None:
                lang = lang.groups()[0]
                text = text[len(lang)+2:]

            try:
                text = pygmentize(text, language=lang)
            except ClassNotFound:
                # no matching lexer found, simply put the code in a <pre> tag
                # (text needs to be escaped)
                text = pygmentize(text, 'text')

            id = self.shelve(text)
            _text = _text.replace(match, id)
        return _text
pygtiler = Pygtiler()

def textile(*args, **kwargs):
    return pygtiler.textile(*args, **kwargs)
