from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

from reportingon.watched.models import Watched, SavedSearch
from reportingon.questions.models import Question
from reportingon.views import *

from tagging.models import Tag, TaggedItem

def home(request):
    if not request.user.is_authenticated():
        questions = Question.objects.all()[:2]
        return render_to_response('home-not-logged-in.html', locals(), context_instance=RequestContext(request))
    watched = Watched.objects.filter(user=request.user)
    return render_to_response('home-logged-in.html', locals(), context_instance=RequestContext(request))

def search(request, query):
    try:
        if (query == ''):
            query = request.GET['query']
        results = Question.search.query(query)
        context = {'questions': list(results), 'query': query, 'search_meta': results._sphinx}
    except:
        context = {'questions': list()}
    return render_to_response('search.html', context, context_instance=RequestContext(request))

def user(request, user):
    user = get_object_or_404(User, username=user)
    if user == request.user:
        profile = True
    return render_to_response('user.html', locals(), context_instance=RequestContext(request))

def beats(request, beat):
    if not beat:
        beats = Tag.objects.all()
        return render_to_response('beats.html', locals(), context_instance=RequestContext(request))
    else:
        beat = get_object_or_404(Tag, name=beat)
        questions = TaggedItem.objects.get_by_model(Question, beat)
        return render_to_response('beat.html', locals(), context_instance=RequestContext(request))