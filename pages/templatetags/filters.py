# coding: utf-8
import re
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.safestring import mark_safe
from django import template
from django.utils.translation import ugettext as _
from limited.utils.utils import isiterable
from limited.markup import parse as parser

register = template.Library()

def iter_find(_str, to_find, n=0):
    """ Finds all occurences of `to_find` in `_str`. Itering-ready. """
    _str_len = len(_str)
    to_find_len = len(to_find)
    while n <= _str_len:
        if _str[n:n+to_find_len] == to_find:
            yield n
        n += 1

def ireplace(text, old, new=':%s:'):
    """ Replaces as occurences of `old` with the string pattern `new`.
        The `new` variable has to be a string containing a placeholder
        where the matches go (`%s`). """
    assert(isinstance(text, basestring) and isinstance(old, basestring)
           and '%s' in new)

    old_len = len(old)
    to_replace = []
    for match in iter_find(text.lower(), old.lower()):
        match = text[match:match+old_len]
        if match not in to_replace:
            to_replace.append((match, new % match))
    for rule in to_replace:
        text = text.replace(*rule)
    return text

def fill(string, n, char, position=1):
    """
    Fills `string` with `char` up to `n` chars (`string` and `char` can be of
    any `str`-compatible type).
    If `position` is 1 (or boolean `True`), the filling chars will be prepended,
    otherwise, they'll be appended.

    Examples:

    >>> fill(1, 3, 0)
    '001'
    >>> fill("Hello", 10, " ")
    '     Hello'
    >>> fill("World", 10, ".", 0)
    'World.....'
    """
    string, char = map(str, (string, char))
    if len(string) >= n:
        return string
    if position:
        # first fill and then string
        return char*(n-len(string))+string
    else:
        # first string and then fill
        return string+char*(n-len(string))

def fill_n(string, n):
    return fill(string, n, 0)

def listnotempty(iterable):
    """ Returns `True` if the list `value` is not an empty one """
    return iterable and isiterable(iterable)

def listlengthisone(value):
    """ Returns `True` if the list `value`'s length is exactly one """
    return len(value) == 1

def humanize_number(n):
    """ Returns a humnized value for numbers up to 3 or `n` """
    strings = (_('zero'), _('one'), _('two'), _('three'), _('four'), _('five'))
    if len(strings) <= n:
        return n
    else:
        return strings[int(n)]

def monthname(value):
    """ Returns the month specified by `value` as string """
    if not value:
        return value
    try:
        return (
            _("January"), _("February"), _("March"), _("April"),
            _("May"), _("June"), _("July"), _("August"),
            _("September"), _("October"), _("November"), _("December")
        )[int(value)-1]
    except (IndexError, TypeError):
        return value

def humanize(value, *values):
    """
    Humanizes `value` (and/or `values`).
    (Currently handles `datetime.datetime` and `int` objects)
    """
    if isinstance(value, datetime):
        if values:
            return _humanize_date(value, values[0])
        else:
            return _humanize_date(value)
    if isinstance(value, int):
        return humanize_number(value)
    return value

def _humanize_date(date1, date2=None):
    """ Humanize `date1` (depending on (`date2` or current date)) """
    if not isinstance(date1, datetime):
        return date1
        # fail silently

    if date2 is None:
        date2 = datetime.now()
    hdate = {}

    delta = relativedelta(date(date1.year, date1.month, date1.day),
                            date(date2.year, date2.month, date2.day))

    if abs(delta.days) in range(2) and delta.years == delta.months == 0:
        hdate['date'] = (_('today'), _('yesterday'), _('two days ago'))[abs(delta.days)]
    else:
        hdate['date'] = "on %s. %s %s" % (date1.day, monthname(date1.month),
                                          date1.year)
    return "%s @%s" % (
        hdate['date'],
        ':'.join([fill(i, 2, 0) for i in date1.hour, date1.minute])
    )

def join(items, string, key=None):
    """
    Joins `items` on `string` intelligently. If `key` is given, uses this
    attribute to join instead.
    >>> join(range(5), " ") == " ".join(map(str, range(5)))
    True
    >>> join(range(5), " ||__class__") == " ".join(map(lambda x:str(x.__class__), range(5)))
    True
    >>> join(([1, 2, (3, 4, 5)], [6, 7, 8, 9, 10]), " ||2") == " ".join(map(str, ((3,4,5), 8)))
    True
    """
    string = string.split('||')
    if len(string) > 1:
        string, key = string
        try:
            key = int(key)
        except ValueError, e:
            from operator import attrgetter
            getter = attrgetter(key)
        else:
            from operator import itemgetter
            getter = itemgetter(key)
        return string.join(map(lambda x:str(getter(x)), items))
    else:
        return string[0].join(map(str, items))


def highlight(text, words):
    """
    Highlights `words` in `text` (puts a html 'highlight' class around that
    words). Case-insensitive.
    """
    text = re.sub(r'<[^<]*?/?>', '', text)
    for word in words:
        text = ireplace(text, word, '<span class="highlight">%s</span>')
    return mark_safe(text)

def parse(value, *args, **kwargs):
    """ A template shortcut to `limited.utils.markup.parse """
    return parser(value, *args, **kwargs)

for filter in (monthname, humanize_number, humanize, listlengthisone,
               listnotempty, fill, highlight, parse, join, fill_n):
    register.filter(filter)
