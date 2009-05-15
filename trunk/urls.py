from django.conf.urls.defaults import *
from django.contrib import admin
from reportingon import settings
from reportingon.views import *

admin.autodiscover()

urlpatterns = patterns('',
    (r'^user/', include('django_authopenid.urls')),
    (r'^questions/', include('questions.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^/?$', home),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
