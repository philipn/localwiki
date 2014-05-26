from django.conf.urls import *
from django.views.generic import ListView

from localwiki.utils.views import NamedRedirectView
from localwiki.utils.constants import DATETIME_REGEXP

from tags.views import PageTagSetUpdateView, PageTagSetVersions,\
    PageTagSetVersionDetailView, PageTagSetCompareView, PageTagSetRevertView

from .views import *
from .feeds import PageChangesFeed, PageFileChangesFeed
from . import models
from .models import Page
from .views import PageFilebrowserView


def slugify(func):
    """
    Applies custom slugify to the slug and stashes original slug
    """
    def wrapped(*args, **kwargs):
        if 'slug' in kwargs:
            kwargs['original_slug'] = kwargs['slug']
            kwargs['slug'] = models.slugify(kwargs['slug'])
        return func(*args, **kwargs)
    return wrapped


urlpatterns = patterns('',
    ###########################################################
    # Files URLs
    # TODO: break out into separate files app with own URLs
    # TODO: shouldn't some of these be _history and not _info?
    ###########################################################
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/$', slugify(PageFileListView.as_view()),
        name='filelist'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_revert/(?P<version>[0-9]+)$',
        slugify(PageFileRevertView.as_view()), name='file-revert'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_upload$',
        slugify(upload), name='file-upload'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_info/$',
        slugify(PageFileInfo.as_view()), name='file-info'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_info/_feed/*$',
        PageFileChangesFeed(), name='file-changes-feed'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_info/compare',
        slugify(PageFileCompareView.as_view())),
    url((r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_info/'
            r'(?P<version1>[0-9]+)\.\.\.(?P<version2>[0-9]+)?$'),
        slugify(PageFileCompareView.as_view()), name='file-compare-revisions'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_info/'
        r'(?P<date1>%s)\.\.\.(?P<date2>%s)?$'
        % (DATETIME_REGEXP, DATETIME_REGEXP),
        slugify(PageFileCompareView.as_view()), name='file-compare-dates'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_info/(?P<version>[0-9]+)$',
        slugify(PageFileVersionDetailView.as_view()),
        name='file-as_of_version'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)/_info/(?P<date>%s)$'
        % DATETIME_REGEXP, slugify(PageFileVersionDetailView.as_view()),
        name='file-as_of_date'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_files/(?P<file>.+)$', slugify(PageFileView.as_view()),
        name='file'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_upload', slugify(upload), name='upload-image'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_filebrowser/(?P<filter>(files|images))$',
        slugify(PageFilebrowserView.as_view()), name='filebrowser'),

    ##########################################################
    # Page tags
    ##########################################################
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/$', slugify(PageTagSetUpdateView.as_view()),
        name='tags'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/_history/$',
        slugify(PageTagSetVersions.as_view()), name='tags-history'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/_history/(?P<version>[0-9]+)$',
        slugify(PageTagSetVersionDetailView.as_view()),
        name='tags-as_of_version'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/_history/(?P<date>%s)$'
        % DATETIME_REGEXP, slugify(PageTagSetVersionDetailView.as_view()),
        name='tags-as_of_date'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/_history/compare',
        slugify(PageTagSetCompareView.as_view())),
    url((r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/_history/'
            r'(?P<version1>[0-9]+)\.\.\.(?P<version2>[0-9]+)?$'),
        slugify(PageTagSetCompareView.as_view()), name='tags-compare-revisions'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/_history/'
        r'(?P<date1>%s)\.\.\.(?P<date2>%s)?$'
        % (DATETIME_REGEXP, DATETIME_REGEXP),
        slugify(PageTagSetCompareView.as_view()), name='tags-compare-dates'),
     url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_tags/_revert/(?P<version>[0-9]+)$',
        slugify(PageTagSetRevertView.as_view()), name='tags-revert'),

    #########################################################
    # History URLs.
    # TODO: Non-DRY. Break out into something like
    # ('/_history/',
    #  include(history_urls(list_view=..,compare_view=..)))?
    #########################################################
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_history/compare',
        slugify(PageCompareView.as_view())),
    url((r'^(?P<region>[^/]+?)/(?P<slug>.+)/_history/'
            r'(?P<version1>[0-9]+)\.\.\.(?P<version2>[0-9]+)?$'),
        slugify(PageCompareView.as_view()), name='compare-revisions'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_history/(?P<date1>%s)\.\.\.(?P<date2>%s)?$'
        % (DATETIME_REGEXP, DATETIME_REGEXP),
        slugify(PageCompareView.as_view()), name='compare-dates'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_history/(?P<version>[0-9]+)$',
        slugify(PageVersionDetailView.as_view()), name='as_of_version'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_history/(?P<date>%s)$' % DATETIME_REGEXP,
        slugify(PageVersionDetailView.as_view()), name='as_of_date'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_history/_feed/*$', PageChangesFeed(),
        name='changes-feed'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_history/$', slugify(PageVersionsList.as_view()),
        name='history'),

    ##########################################################
    # Basic edit actions.
    ##########################################################
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_edit$', slugify(PageUpdateView.as_view()),
        name='edit'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_delete$', slugify(PageDeleteView.as_view()),
        name='delete'),
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_revert/(?P<version>[0-9]+)$',
        slugify(PageRevertView.as_view()), name='revert'),

    url(r'^(?P<region>[^/]+?)/_create$', PageCreateView.as_view(), name='create'),

    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_rename$', PageRenameView.as_view(), name='rename'),

    ##########################################################
    # Permissions
    ##########################################################
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+)/_permissions$', slugify(PagePermissionsView.as_view()),
        name='permissions'),


    # Random page
    url(r'^tools/(?i)Random_Page/*$', PageRandomView.as_view(), name='random'),

    # Catch-all and route to a page.
    url(r'^(?P<region>[^/]+?)/(?P<slug>.+?)/*$', slugify(PageDetailView.as_view()),
        name='show'),
)


