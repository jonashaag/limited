"""
    limited.widgets
    ~~~~~~~~~~~~~~~

    limited has a very, very basic plugin-like widgets system. That widgets
    are displayed in the sidebar.

    You can add your widget by simply dropping a file named
    somewhat_widget.html in /user_templates/widgets/.
    The order can be set in the `WIDGET_CONFIGURATION` dict in `limited.settings`.

    Note: Native widgets (hence, widgets provided by this blog system) will be
    overwritten if you use the same file name for your widget.
"""
import os
from limited.settings import WIDGETS_DIR, USER_TEMPLATES_DIR, TEMPLATE_DIRS
from limited.exceptions import WidgetNotFound
try:
    from limited.settings import WIDGET_CONFIGURATION
except ImportError:
    WIDGET_CONFIGURATION = {}

WIDGET_DIRS = map(lambda dir:os.path.join(dir, WIDGETS_DIR), TEMPLATE_DIRS)
WIDGET_LIST_FILE = os.path.join(USER_TEMPLATES_DIR, WIDGETS_DIR, 'widgets')

class Widget(object):
    """ Holds a widget template """
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.path = os.path.join(directory, filename)
        self.name = os.path.basename(filename)[:-5]
        # strip off ".html"

    def shall_include(self, to_exclude):
        return self.filename not in to_exclude and self.path not in to_exclude

    def __eq__(self, other):
        """
        This `__eq__` method is defined in order that you can use
        >>> 'mywidget.html' == Widget('mywidget.html', 'somepath')
        True
        or
        >>> 'widget.html' in (Widget('foo.html', 'p'), Widget('bar.html', 'p'))
        False
        """
        if isinstance(other, Widget):
            return self.filename == other.filename
        return self.filename == other

def append_html(s):
    if s.endswith('.html'):
        return s
    return s+'.html'

def find_widgets(widgets=None):
    if widgets is None:
        widgets = []
    for directory in WIDGET_DIRS:
        for widget in os.listdir(directory):
            if widget.endswith('.html'):
                    if widget not in widgets:
                        widgets.append(Widget(widget, directory))
    return widgets

def find_widget(name):
    for directory in WIDGET_DIRS:
        if os.path.exists(os.path.join(directory, name)):
            return Widget(name, directory)
    raise WidgetNotFound("The widget '%s' was not found" % name)

def get_widgets():
    """
    Returns a list of `Widget` objects ordered by the
    `limited.settings.WIDGET_CONFIGURATION['order'] tuple.
    Widgets not appearing in that list will be appended unordered.
    """
    exclude = WIDGET_CONFIGURATION.get('exclude') or tuple()
    include = WIDGET_CONFIGURATION.get('include') or tuple()
    order = WIDGET_CONFIGURATION.get('order') or tuple()
    # (not using `.get(key, tuple())` here to avoid "not-iterable" errors we'd
    # get for the `in` statement few lines below if someone sets e.g. `None`)

    if exclude == 'all':
        # user said (s)he doesn't want any widgets to be included,
        # so don't import any widget but the ones (s)he defined in `include`.
        return map(find_widget, map(append_html, include))
    else:
        # first, import all widgets listed in `widget_order` and then add all
        # the other widgets found by directory scanning to the widget list.
        # (also, exclude all widgets defined in `exclude`.)
        return filter(lambda widget:widget.shall_include(exclude),
                      find_widgets(map(find_widget, map(append_html, order))))
