from django.conf.urls.defaults import *
from django.contrib import admin
from reportingon import settings
from reportingon.views import *

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^questions/', include('reportingon.questions.urls')),
    (r'^answers/', include('django.contrib.comments.urls')),
    (r'^user/', include('django_authopenid.urls')),
    (r'^beats/?(?P<beat>[^/]+)?$', beats),
    (r'^admin/(.*)', admin.site.root),
    (r'^search/(.*)', search),
    (r'^users/(.*)', user),
    (r'^/?$', home),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
