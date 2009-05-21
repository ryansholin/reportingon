from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^$', list_questions),
    (r'^new/?$', new_question),
    (r'^edit/(?P<qid>[\d]+)', edit_question),
    (r'^delete/(?P<qid>[\d]+)', delete_question),
    (r'^(?P<qid>[\d]+)', view_question),
)
