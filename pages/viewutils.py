from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader as tmpl_loader
from models import Page, Comment
from limited.utils import utils
from django.conf import settings
from limited.pages import make_request_context

def render_to_response(template, parameters=None, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    parameters.update(kwargs)
    return HttpResponse(utils.shorten_html(
        tmpl_loader.render_to_string(template, make_request_context(parameters))),
        **httpresponse_kwargs)

def paginate(pages, page):
    """ Crazy shidd O__O """
    if len(pages) <= 6:
        return pages
    if page <= 3:
        return pages[:4]+['...']+pages[-2:]
    elif page >= len(pages)-3:
        return pages[:2]+['...']+pages[-4:]
    else:
        return pages[:2]+['...']+pages[page-2:page+2]+['...']+pages[-2:]

def get_popular_pages(isblog=False):
    """
        Get Page items marked as popular
        @param isblog: `True` if only blog entries should be returned
        @returns: a list of NavLink instances containing the links
    """
    return Page.filter(popular=True).order_by('-creation_time')

def get_latest_comments(n=5):
    return Comment.objects.order_by('-creation_time').filter(public=True)[:n]

def render(template, current=None, parameters={}, paginize=False,
           page=None, items_per_page=None, mimetype='text/html'):
    """ Generate navi and render the template """
    parameters.update({
        'template' : template,
        'navigation_current': current,
    })

    if paginize:
        if page is None:
            raise MissingPageIndex()
        items_per_page = items_per_page or settings.ENTRIES_PER_PAGE
        paginator = Paginator(parameters['items'], items_per_page)
        parameters['items'] = paginator.page(page).object_list
        parameters['page'] = page
        parameters['pagecount'] = paginate(paginator.page_range, page)
        if page > 1:
            parameters['previous_page'] = page-1
        if page < len(paginator.page_range):
            parameters['next_page'] = page+1
    else:
        try:
            if len(parameters['items']) == 1:
                parameters['issingle'] = True
                parameters['item'] = parameters['items'][0]
        except KeyError:
            pass

    parameters['emtpy_query'] = not parameters.get('items', True)

    return render_to_response(template, parameters, mimetype=mimetype)
