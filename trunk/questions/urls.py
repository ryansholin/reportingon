from django.conf.urls.defaults import *
from django.contrib import admin

from views import *

urlpatterns = patterns('',
    (r'^$', questions_home),
    (r'^(?P<qslug>)', question_view),
    (r'^new/$', create_question),
    (r'^update/(?P<qid>[\d])', update_question),
    (r'^delete/(?P<qid>[\d])', delete_question),
)