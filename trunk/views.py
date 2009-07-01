from django.contrib.contenttypes.models import ContentType

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

from reportingon.rated.models import Rated
from reportingon.watched.models import Watched, SavedSearch
from reportingon.questions.models import Question
from reportingon.views import *

from tagging.models import Tag, TaggedItem

from utils.activity import * # these are utils that collect activity

def home(request):
    if not request.user.is_authenticated():
        questions = Question.objects.all()[:2]
        return render_to_response('home-not-logged-in.html', locals(), context_instance=RequestContext(request))
        
    watched = Watched.objects.filter(user=request.user, status=1)
    watched_activity = list()
    for obj in watched:
        if obj.content_type.model == 'user':
            user = User.objects.get(id=obj.object_id)
            if request.user is not user:
                watched_activity.extend(get_recent_activity_for_user(user, thirdPerson=True)) # don't sort, use 3rd person
        elif obj.content_type.model == 'question':
            watched_activity.extend(get_recent_activity_for_question(Question.objects.get(id=obj.object_id)))
            
    watched_activity = uniqueify(watched_activity, lambda x:x['id'])
    watched_activity.sort(key=lambda x:x['date'], reverse=True)
    
    # hard limit on 30
    watched_activity = watched_activity[:100]
    
    return render_to_response('home-logged-in.html', locals(), context_instance=RequestContext(request))

def search(request, query):
    if (query == ''):
        query = request.GET['query']
    raw_results = Question.search.query(query)
    results = raw_results[0:raw_results.count()] # need to implicitly slice it in order to access the full results...djangosphinx FAIL
    try:
        search_obj = SavedSearch.objects.get(query__exact=query)
    except:
        search_obj = None
    context = {'questions': results, 'query': query, 'search_meta': raw_results._sphinx, 'search_obj': search_obj}
    return render_to_response('search.html', context, context_instance=RequestContext(request))

def user(request, user, edit):
    
    user = get_object_or_404(User, username=user)
    if user == request.user:
        profile = True
        
    if not edit:
        recent_activity = get_recent_activity_for_user(user, True) # sort = true
    
    answer_content_type = ContentType.objects.get(name='comment')
    question_content_type = ContentType.objects.get(name='question')
    
    user_questions = Question.objects.filter(author=user).count()
    user_answers = Comment.objects.filter(user=user).count()
    user_liked_questions = Rated.objects.filter(content_type=question_content_type.id, rated_user=user).count()
    user_liked_answers = Rated.objects.filter(content_type=answer_content_type.id, rated_user=user).count()
    
    if edit:
        
        from reportingon.utils.models import UserProfile
        from reportingon.utils.forms import UserProfileForm
        
        profile = UserProfile.objects.get(user=request.user)
        
        if (request.POST):
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()
                return HttpResponseRedirect(request.user.get_absolute_url())
        else:
            form = UserProfileForm(instance=profile)
        
        return render_to_response('user-edit.html', locals(), context_instance=RequestContext(request))
    else:
        return render_to_response('user.html', locals(), context_instance=RequestContext(request))

def beats(request, beat):
    if not beat:
        beats = Tag.objects.all()
        return render_to_response('beats.html', locals(), context_instance=RequestContext(request))
    else:
        beat = get_object_or_404(Tag, name=beat)
        questions = TaggedItem.objects.get_by_model(Question, beat)
        return render_to_response('beat.html', locals(), context_instance=RequestContext(request))
