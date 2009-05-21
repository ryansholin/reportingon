from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment

from reportingon.questions.models import Question

def home(request):
    if not request.user.is_authenticated():
        return render_to_response('home-not-logged-in.html', locals(), context_instance=RequestContext(request))
    
    return render_to_response('home-logged-in.html', locals(), context_instance=RequestContext(request))

def search(request, query): 
    try:
        if (query == ''):
            query = request.GET['query']
        results = Question.search.query(query)
        context = {'results': list(results), 'query': query, 'search_meta': results._sphinx}
    except:
        context = {'results': list()}
    return render_to_response('search.html', context, context_instance=RequestContext(request))

def user(request, user):
    profile = True
    return render_to_response('user.html', locals(), context_instance=RequestContext(request))
