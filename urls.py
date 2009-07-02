from django.conf.urls.defaults import *
from django.contrib import admin
from reportingon import settings
from reportingon.views import *
from reportingon.watched.views import *
from reportingon.feeds import LatestQuestions, LatestQuestionsByBeat, LatestQuestionsBySearch, LatestAnswersByQuestion, LatestQuestionsByUser

admin.autodiscover()

import useradmin

feeds = {
    'latest': LatestQuestions,              # /feeds/latest 
    'beat': LatestQuestionsByBeat,          # /feeds/beat/beat terms here
    'search': LatestQuestionsBySearch,      # /feeds/search/search terms go here
    'questions': LatestAnswersByQuestion,   # /feeds/questions/16[/slug-is-optional/]
    'users': LatestQuestionsByUser,         # /feeds/users/Pete
}

urlpatterns = patterns('',
    (r'^feeds/watched/(?P<username>.*)/?', watched_feed),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^questions/', include('reportingon.questions.urls')),
    (r'^answers/', include('django.contrib.comments.urls')),
    (r'^user/', include('django_authopenid.urls')),
    (r'^watch/', include('reportingon.watched.urls')),
    (r'^rate/', include('reportingon.rated.urls')),
    (r'^save-search/?(?P<query>[^/]+)?', save_search),
    (r'^beats/?(?P<beat>[^/]+)?$', beats),
    (r'^users/?(?P<user>[^/]+)?/?(?P<edit>[^/]+)?', user),
    (r'^admin/(.*)', admin.site.root),
    (r'^search/(.*)', search),
    (r'^/?$', home),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
