import os
from collections import defaultdict
from django.conf import settings
from limited.settings import DEFAULT_CONTEXT_VARIABLES, MEDIA_ROOT
from limited import _internal

class GroupedDict(defaultdict):
    def __init__(self, iterable, groupby=lambda x:x):
        self.default_factory = list
        for k, v in iterable:
            self[groupby(k)].append(v)

class HomePage(object):
    absolute_url = ''
    title = 'Home'

def find_static_files(root_dirs=None):
    """ Return all .js and .css files in `MEDIA_ROOT` """
    if root_dirs is None:
        root_dirs = []
    current_dir = os.path.join(MEDIA_ROOT, *root_dirs)

    for _file in os.listdir(current_dir):
        if os.path.isfile(os.path.join(current_dir, _file)):
            if _file.endswith('.css'):
                yield 'css', os.path.join(*(root_dirs+[_file]))
            elif _file.endswith('.js'):
                yield 'js', os.path.join(*(root_dirs+[_file]))
        else:
            for _type, fname in find_static_files(root_dirs+[_file]):
                yield _type, fname


def make_request_context(dic=None):
    from limited.utils import widgets
    from models import Page, Tag, User
    from viewutils import get_latest_comments

    if dic is None:
        dic = {}

    static_files = GroupedDict(find_static_files())

    dic.update((key, getattr(settings, key)) for key in (
        'BLOG_URL', 'MEDIA_URL', 'ADMINS', 'USE_PYGMENTS'
    ))
    dic.update(DEFAULT_CONTEXT_VARIABLES)
    dic.update({
        'navigation_top' : [HomePage()]+list(Page.filter(in_navigation=True)),
        'tags' : Tag.objects.all().order_by('-name'),
        'latestcomments' : get_latest_comments(),
        'popular_pages' : Page.filter(popular=True),
        'WIDGETS' : widgets.get_widgets(),
        'JS_FILES' : static_files['js'],
        'CSS_FILES' : static_files['css'],
        'limited' : _internal.software_info()
    })

    if not 'COPYRIGHT_YEARS' in dic:
        from datetime import datetime
        dic['COPYRIGHT_YEARS'] = [datetime.now().year]
    assert(0 < len(dic['COPYRIGHT_YEARS']) < 3)
    # two years at maximum

    return dic
