# coding: utf-8
"""
    limited.utils.utils
    ~~~~~~~~~~~~~~~~~~~
"""
import os
import random
import re
from urllib import quote_plus as htmlencode, unquote_plus as htmldecode
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict

def isiterable(iterable):
    """ Returns `True` if `iterable` is iterable """
    try:
        iter(iterable)
        return True
    except TypeError:
        return False

def shorten_html(s):
    """
    Strip line-leading whitespace and empty lines.
    Don't strip stuff within HTML <pre> blocks.
    >>> shorten_html(\"""
    Hello

        there
    \""")
    "Hello\n    there"

    >>> shorten_html(\"""
    Hello

        there
    <pre>
    a
        pre

            block
    </pre>
    \""")
    "Hello\n    there\n<pre>\na\n    pre\n\n        block\n</pre>"
    """
    def generate_token(index):
        return '__SHORTEN_HTML_TOKEN_%s__' % index

    blocks = []
    for regexp in ('<table class="codetable">(.+?)</table>', '<pre>(.+?)</pre>'):
        blocks += re.findall(regexp, s, re.DOTALL)
        for index, block in enumerate(blocks):
            s = s.replace(block, generate_token(index))

    stripped = '\n'.join([l.strip() for l in s.split('\n')]).replace('\n\n', '\n')
    for index in re.findall('__SHORTEN_HTML_TOKEN_(\d+)__', s):
        stripped = stripped.replace(generate_token(index), blocks[int(index)])
    return stripped

def escape_mail(mail):
    """ Escape email adress to prevent spamming """
    at_escapes = ('at ', 'ät', 'at sign', 'ä_t', '[guesswhat]', '[at]')
    dot_escapes = ('dot', '_dot_', 'point', '[dot]')
    mail = mail.replace('@', random.choice(at_escapes).center(3))
    return mail.replace('.', random.choice(dot_escapes).center(3))

def makepath(path):
    """ Same as os.makedirs, but doesn't throw an exception
        if folder already exists """
    dpath = normpath(dirname(path))
    if not exists(dpath): makedirs(dpath)
    return normpath(abspath(path))

def join_current_path(*paths):
    return os.path.join(join_current_path.BASE_DIR, *paths)

class SortedDefaultDict(SortedDict):
    """ A SortedDict holding default values """
    def __init__(self, _type=None, *args, **kwargs):
        self._type = _type
        SortedDict.__init__(self, *args, **kwargs)

    def __missing__(self, key):
        if self._type is None:
            return None
        return self._type()

    def sort_by_values(self, **kwargs):
        self.keyOrder = [key for key, value in
            sorted(self.iteritems(), key=lambda item:item[1], **kwargs)]
