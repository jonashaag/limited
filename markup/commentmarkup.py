"""
    Uuuuugly.

    A very basic markup module to parse comment markup.
    Features are only:
     * *bold text*
     * _italic text_
     * [http://example.org links]
"""
from pyparsing import ParseFatalException, QuotedString
from limited.settings import SECRET_KEY
from hashlib import md5
from time import time

def parse_quotes(s, quote_char='>'):
    parsed = []
    previous_line = None
    for line in s.split('\n'):
        if line.startswith(quote_char):
            line = line[1:].strip()
            if not line:
                continue
            if previous_line is not None:
                previous_line[1] += '\n' + line
            else:
                previous_line = [True, line]
                parsed.append(previous_line)
        else:
            parsed.append([False, line])
            previous_line = None

    return parsed


def escape(s, quote=False, append_newline=True):
    # this is cgi.escape, modified
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    if quote:
        s = s.replace('"', "&quot;")
    if append_newline:
        s += '\n'
    return s


def to_html(opening, closing):
    def handle_action(s, l, t):
        return opening + t[0] + closing
    return handle_action

def to_link(s, l, t):
    try:
        url, text=t[0].split(" ", 1)
    except ValueError:
        url = text = t[0]
    return '<a href="%s" title="%s">%s</a>' % (url, text, text)

italicized = QuotedString('_').setParseAction(to_html('<i>','</i>'))
bolded = QuotedString('*').setParseAction(to_html('<b>','</b>'))
urlified = QuotedString('[', endQuoteChar=']').setParseAction(to_link)

markup_handler = urlified | bolded | italicized

QUOTE_TEMPLATE = ('<span class="commentinlinequoteword">Zitat:</span>'
                  '<span class="commentinlinequote">%s</span>')

def parse_comment(string):
    # This function is... *kotz*
    def gen():
        for isquote, lines in parse_quotes(string.replace('\r\n', '\n').strip('\n')):
            if not lines: continue
            if not isquote:
                yield '<p>%s</p>' % lines
            else:
                yield QUOTE_TEMPLATE % lines

    return markup_handler.transformString(''.join(gen()))

parse_string = parse_comment
