from django.conf.urls.defaults import *
from django.contrib import admin

from reportingon.views import *
from reportingon import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^account/', include('registration.urls')),
    (r'^question(s?)/', include('questions.urls')),
    (r'^$', home),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )