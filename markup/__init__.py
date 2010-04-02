# coding: utf-8
"""
    limited.markup
    ~~~~~~~~~~~~~~
    This module handles all markup-relevant stuff. It offers a simple API
    (two functions, `parse` and `parse_comment`) for parsing texts written
    in a markup language.

    The comments should be parsed with an very restricted markup parser
    (like `limited.markup.commentmarkup`) because using a full-featured one,
    users could vandalize using very big font sizes or damaging your layout
    in other ways.
"""
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import commentmarkup
from django.contrib.markup.templatetags import markup as django_markup

register = template.Library()

def pygtile(*args, **kwargs):
    import pygtile
    return pygtile.textile(*args, **kwargs)

MARKUP_PARSERS = {
    'markdown' : django_markup.markdown,
    'restructuredtext' : django_markup.restructuredtext,
    'rest' : django_markup.restructuredtext,
    'textile' : pygtile
}

@register.filter
def parse_comment(value):
    """
    Parse a blog post comment using `commentmarkup.parse` function.
    """
    try:
        return mark_safe(commentmarkup.parse(value))
    except ValueError:
        return value

@register.filter
def parse(*args, **kwargs):
    """
    Parse the given text using the markup parser defined in
    `settings.MARKUP_PARSER` (or `limited.markup.pygtile`, if none was set).
    """
    if hasattr(settings, 'MARKUP_PARSER'):
        parser = settings.MARKUP_PARSER
        if not callable(parser):
            parser = MARKUP_PARSERS.get(parser, 'textile')
    else:
        parser = MARKUP_PARSERS['textile']
    try:
        return mark_safe(parser(*args, **kwargs))
    except Exception as e:
        raise RuntimeError(str(e))
