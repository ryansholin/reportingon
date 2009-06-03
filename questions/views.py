from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from forms import QuestionForm
from models import Question

def list_questions(request):
    questions = Question.objects.all()
    return render_to_response('list-questions.html', locals(), context_instance=RequestContext(request))

def view_question(request, qid):
    question = Question.objects.get(id__exact=qid)
    question.content_type = ContentType.objects.get_for_model(Question)
    return render_to_response('view-question.html', locals(), context_instance=RequestContext(request))

@login_required
def new_question(request):
    if(request.POST):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.slug = slugify(question.question)
            question.status = 1
            question.save()
            return HttpResponseRedirect(reverse(view_question, args=[question.pk, question.slug]))
    else:
        form = QuestionForm()
    
    return render_to_response('new-question.html', locals(), context_instance=RequestContext(request))

@login_required
def edit_question(request, qid):
    if(request.POST):
        question = Question.objects.get(id__exact=qid)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(reverse(view_question, args=[question.pk]))
    else:
        question = Question.objects.get(id__exact=qid)
        form = QuestionForm(instance=question)
    return render_to_response('edit-question.html', locals(), context_instance=RequestContext(request))

@login_required
def delete_question(request, qid):
    question = Question.objects.get(id__exact=qid)
    question.delete()
    return HttpResponseRedirect('/questions')
