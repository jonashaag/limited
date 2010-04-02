# coding: utf-8
"""
    limited.pages.views
    ~~~~~~~~~~~~~~~~~~~
"""
import re
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse as urlreverse
from limited.settings import MEDIA_ROOT, ADMINS, IP_BLACKLIST, WORD_BLACKLIST
from limited import responses
from limited.pages.models import Comment, Page
from limited.utils.utils import SortedDefaultDict
from limited.pages.viewutils import render, get_popular_pages
from limited.pages.wrappers import Year
from django.conf import settings

def split_tags(tags):
    return tags.split(',')

def posts_by_tags(tags=None, tag=None):
    """ Get posts by tag(s) """
    tags = tags or (tag,)
    if tags is None:
        tags = request.GET.get('tags')
        if tags is None:
            raise Http404

    if len(tags) == 1:
        return Page.filter(isblog=True, tags__slug=tags[0])
    else:
        return Page.filter(isblog=True,
                           tags__slug__in=tags).order_by('-creation_time')

def by_tags(request, tags=None, tag=None):
    tags = split_tags(tags or tag)
    return render(settings.TEMPLATE_SEARCH, 'by_tags', parameters={
        'keywords': tags, 'results': posts_by_tags(tags)
    })

def search(request, keywords=None, sep=' '):
    """ Search for `keywords` in `Page` titles and `contents` """
    if keywords is None:
        keywords = request.GET.get('keywords')
        # prefer GET to POST
        if keywords is None:
            keywords = request.POST.get('keywords')
            if not keywords:
                # no (NOT EVEN A LITTLE BIT!!!!!!!1111!!1) input
                return HttpResponseRedirect(urlreverse(home))
    assert(isinstance(keywords, basestring))
    if not re.match('[a-zA-Z]', keywords):
        return HttpResponseRedirect(urlreverse(home))
    keywords = kewwords.strip().strip(',')
    if not keywords:
        return HttpResponseRedirect(urlreverse(home))

    results = SortedDefaultDict(int)
    keywords = keywords.split(sep)

    for keyword in keywords:
        for obj in Page.filter(title__contains=keyword):
            results[obj] += 5
        for obj in Page.filter(text__contains=keyword):
            results[obj] += obj.text.lower().count(keyword.lower())
    results.sort_by_values(reverse=True)

    return render(settings.TEMPLATE_SEARCH, 'search', parameters={
        'keywords': keywords, 'results': results
    })

def single_page(request, single):
    """ Display single page having slug `single` or raise 404 """
    page = get_object_or_404(Page.filter(url=single, isblog=False))
    return render(settings.TEMPLATE_PAGE, single, {
        'items' : (page,)
        #'comment_url' : urlreverse('comment', kwargs = {'single' : single}),
    })

def all_pages(request):
    """ Display *all* pages """
    return render(settings.TEMPLATE_PAGE, None, {
        'items' : Page.filter(isblog=False).oder_by('-creation_time')
    })

def popular_pages(request, isblog=False):
    """
    Display popular pages.
    :param isblog: `True` if only blog entries should be displayed
    """
    template = isblog and settings.TEMPLATE_BLOG or settings.TEMPLATE_PAGE
    return render(template, None, {
        'items' : Page.filter(isblog=isblog, popular=True),
        'isblog': isblog,
    })

def single_post(request, single):
    """ Display single blog entry having slug `single` or raise 404 """
    post = get_object_or_404(Page, url=single, isblog=True)
    return render(settings.TEMPLATE_BLOG, single, {
        'items' : (post,),
        'comment_url' : urlreverse('comment', kwargs = {'single' : single}),
        'comments' : post.comment_set.all().filter(public=True),
    })

def blog_pages(request, page=1, home=False):
    """
        Display blog entries using pagination.
        @param page: the current page's index
        @param home: (template-specific) `True` if using this for
                     displaying the "home" site.
    """
    posts = Page.filter(isblog=True).order_by('-creation_time')
    return render(settings.TEMPLATE_BLOG, ('pages', 'home')[home], {
        'items' : posts,
        'home' : home,
    }, True, int(page))


def comment(request, single):
    """
    Add a comment to a Post having slug `single` (raises 404 of Post
    does not exist).
    """
    is_spam = False
    # blacklist checks:
    if request.META['REMOTE_ADDR'] in IP_BLACKLIST:
        return responses.HttpNotAcceptable("""
            Deine IP-Adresse ist auf einer Blacklist, weil von dieser
            in Vergangenheit massiv gespammt wurde. Bitte kontaktiere
            mich, falls du dich zu Unrecht blockiert fühlst.
        """)
    elif request.method == 'POST':
        name = request.POST['name']
        text = request.POST['text']

        lower_text = text.lower()
        lower_name = name.lower()

        for word in WORD_BLACKLIST:
            if word in lower_name or word in lower_text:
                return responses.HttpNotAcceptable(_("The the word '%s' is "
                    "blacklisted. Please avoid it in your comments.") % word)
        public = True

        if not name or not text:
            return render(settings.TEMPLATE_BLOG, single, {
                'items' : [get_object_or_404(Page, url=single)],
                'error' : _('Please fill out all fields!'),
            })
        comment = Comment()
        comment.page = get_object_or_404(Page, url=single)
        comment.name = name
        comment.text = text
        comment.save()
        return responses.SuccessfullyCommentedResponse(comment.page.url)
    else:
        return HttpResponseRedirect(urlreverse('single_post',
            kwargs={'single': single}))

def home(request):
    """ View for "home" page. """
    return blog_pages(request, page=1, home=True)

def _feed(request, posts, n=20, show_summary=False, show_content=True):
    """ Display news feed, chosen by `type` """
    posts = posts.order_by('-edit_time')
    if posts:
        pubdate = posts.latest(field_name='creation_time').creation_time
    else:
        pubdate = None
    return render(settings.TEMPLATE_FEED, None, {
        'items' : posts[:n],
        'pubdate' : pubdate,
        'show_summary' : show_summary,
        'show_content' : show_content,
        'REQUEST_PATH' : request.path.lstrip('/')
    }, mimetype='application/xml')

def feed(request):
    return _feed(request, Page.filter(isblog=True))

def short_feed(request):
    return _feed(request,
        Page.filter(isblog=True), show_content=False, show_summary=True)

def title_feed(request):
    return _feed(request, Page.filter(isblog=True), show_content=False,
                 show_summary=False)

def feed_by_tags(request, tags=None, tag=None):
    tags = split_tags(tags or tag)
    return _feed(request, posts_by_tags(tags))

def archive(request, year=None, month=None):
    """
    Display post archive.
    :param year: the year to filter by or `None`
    :param month: the month to filter by (requires `year` set) or `None`
    """
    posts = Page.filter(isblog=True)

    if year is None:
        years = {}
        for post in posts:
            _year = years.setdefault(post.creation_time.year,
                                     Year(post.creation_time.year))
            _year.add_month(post.creation_time.month)
        return render(settings.TEMPLATE_OVERVIEW_ARCHIVE, 'archive', {
            'years' : sorted(years.values(), reverse=True),
        })
    else:
        year = int(year)
    if month is not None:
        month = int(month)

    years = set([p.creation_time.year for p in posts])
    posts = posts.filter(creation_time__year=year)
    months = None
    if month:
        months = set([p.creation_time.month for p in posts])
        posts = posts.filter(creation_time__month=month)
    return render(settings.TEMPLATE_ARCHIVE, 'archive', {
        'items' : posts,
        'year' : year,
        'years' : years,
        'month' : month or '',
        'months' : months,
    })
