from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.comments.models import Comment
from django.contrib.comments.forms import CommentForm

def home(request):
    return render_to_response('home_not_logged_in.html', locals(), context_instance=RequestContext(request))

def edit_answer(request, aid):
    answer = Comment.objects.get(id=aid)
    form = CommentForm(instance=answer)
    assert False, form
    return render_to_response('answer_edit.html', locals(), context_instance=RequestContext(request))
