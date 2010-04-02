from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('limited.pages.views',
    # pages stuff:

    #url(r'^pages/$', 'all_pages', name='all_pages'),
    url(r'^pages/popular/$', 'popular_pages', name='popular_pages'),
    url(r'^page/(?P<single>[a-zA-Z0-9-?]+)$', 'single_page', name='single_page'),

    # blog stuff:
    url(r'^posts/by_tag/(?P<tag>[a-zA-Z\d\-_]+)$', 'by_tags', name='by_tag'),
    url(r'^posts/by_tags/(?P<tags>[a-zA-Z\d\-_,]+)$', 'by_tags', name='by_tags'),
    url(r'^posts/search/', 'search', name='search'),
    url(r'^posts/popular/$', 'popular_pages', name='popular_posts', kwargs={'isblog' : True}),
    url(r'^posts/page/(?P<page>[0-9]+)/$', 'blog_pages', name='blog_pages'),
    url(r'^posts/archive/$', 'archive', name='archive'),
    url(r'^posts/archive/(?P<year>\d+)/$', 'archive', name='archive_yearly'),
    url(r'^posts/archive/(?P<year>\d{4})/(?P<month>[0-9]{2})/$', 'archive', name='archive_monthly'),
    url(r'^post/(?P<single>[a-zA-Z\d\-_]+)$', 'single_post', name='single_post'),
    url(r'^post/(?P<single>[a-zA-Z\d\-_]+)/comment$', 'comment', name='comment'),
    url(r'^posts/$', 'blog_pages', name='blog', kwargs={'page' : 1}),

    url(r'^feed/short/$', 'short_feed', name='short_feed'),
    url(r'^feed/title/$', 'title_feed', name='title_feed'),
    url(r'^feed/by_tag/(?P<tag>[a-zA-Z\d\-_]+)$', 'feed_by_tags', name='feed_by_tag'),
    url(r'^feed/by_tags/(?P<tags>[a-zA-Z\d\-_,]+)$', 'feed_by_tags', name='feed_by_tags'),
    url(r'^feed/$', 'feed', name='feed'),

    # admin
    (r'^%s[/]?(.*)$' % settings.ADMIN_URL.strip('/'), admin.site.root),
    #url(r'^stats/', include('limited.stats.urls')),

)

if True:
    from limited.utils.utils import join_current_path
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', name='media', kwargs={
            'document_root': join_current_path('media/')
        })
    )

urlpatterns += patterns('limited.pages.views',
    # home
    url(r'^$', 'home', name='home'),
)
