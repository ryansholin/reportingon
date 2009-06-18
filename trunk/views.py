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
    watched = Watched.objects.filter(user=request.user, status=1)
    return render_to_response('home-logged-in.html', locals(), context_instance=RequestContext(request))

def search(request, query):
    try:
        if (query == ''):
            query = request.GET['query']
        results = Question.search.query(query)
        search_obj = False
        context = {'questions': list(results), 'query': query, 'search_meta': results._sphinx, 'search_obj': search_obj}
    except:
        context = {'questions': list(), 'search_obj': search_obj}
    return render_to_response('search.html', context, context_instance=RequestContext(request))

def user(request, user):
    user = get_object_or_404(User, username=user)
    if user == request.user:
        profile = True
    
    recent_activity = list()
    for obj in Watched.objects.filter(user=user):
        key = obj.created.strftime("%Y-%m-%d %H:%M:%S")
        if obj.content_type.model == 'user': # user is watching a user
            description = """Started watching <a href="#">%s</a>""" % obj.object.username
        elif obj.content_type.model == 'tag':
            description = """Started watching the &ldquo;<a href="#">%s</a>&rdquo; beat""" % obj.object.name
        elif obj.content_type.model == 'question':
            description = """Started watching the question &ldquo;<a href="#">%s</a>&rdquo;""" % obj.object.question
        elif obj.content_type.model == 'savedsearch':
            description = """Started watching the search &ldquo;<a href="#">%s</a>&rdquo;""" % obj.object.query
        else:
            continue
        recent_activity.append({ 'description': description, 'date': obj.created })
        description = ''
            
    for obj in Question.objects.filter(author=user):
        key = obj.created.strftime("%Y-%m-%d %H:%M:%S")
        recent_activity.append({ 'description': """Asked &ldquo;<a href="#">%s</a>&rdquo;""" % obj.question, 'date': obj.created })
        
    for obj in Comment.objects.filter(user=user):
        key = obj.submit_date.strftime("%Y-%m-%d %H:%M:%S")
        # question = get_object_or_404(Question, id=obj.object_pk)
        recent_activity.append({ 'description': """Answered a <a href="#">question</a> with &ldquo;<a href="#">%s</a>&rdquo;""" % obj.comment, 'date': obj.submit_date })
        
    recent_activity.sort(key=lambda x:x['date'], reverse=True)
    
    return render_to_response('user.html', locals(), context_instance=RequestContext(request))

def beats(request, beat):
    if not beat:
        beats = Tag.objects.all()
        return render_to_response('beats.html', locals(), context_instance=RequestContext(request))
    else:
        beat = get_object_or_404(Tag, name=beat)
        questions = TaggedItem.objects.get_by_model(Question, beat)
        return render_to_response('beat.html', locals(), context_instance=RequestContext(request))
