from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment

from reportingon.questions.models import Question
from reportingon.watched.models import Watched
from reportingon.views import *

from tagging.models import Tag, TaggedItem

def home(request):
    if not request.user.is_authenticated():
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
    profile = True
    return render_to_response('user.html', locals(), context_instance=RequestContext(request))

def beats(request, beat):
    if not beat:
        beats = Tag.objects.all()
        return render_to_response('beats.html', locals(), context_instance=RequestContext(request))
    else:
        beat = Tag.objects.get(name=beat)
        beat.content_type = ContentType.objects.get_for_model(Tag)
        questions = TaggedItem.objects.get_by_model(Question, beat)
        return render_to_response('beat.html', locals(), context_instance=RequestContext(request))