from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^$', questions_home),
    (r'^new/?$', create_question),
    (r'^update/(?P<qid>[\d]+)', update_question),
    (r'^delete/(?P<qid>[\d]+)', delete_question),
    (r'^(?P<qid>[\d]+)', question_view),
)
