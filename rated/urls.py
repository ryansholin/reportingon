from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^(?P<content_type_id>[^/]+)?/?(?P<object_id>[^/]+)?/?(?P<rated_user_id>[^/]+)?$', rate),
)
