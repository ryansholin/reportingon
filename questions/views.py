from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from forms import QuestionForm
from models import Question

def questions_home(request):
    questions = Question.objects.all()
    return render_to_response('questions_base.html', locals(), context_instance=RequestContext(request))

def question_view(request, qid):
    question = Question.objects.get(id__exact=qid)
    return render_to_response('question_detail.html', locals(), context_instance=RequestContext(request))

def create_question(request):
    if(request.POST):
        form = QuestionForm(request.POST)
        if form.is_valid():
            try:
                question = form.save()
                return HttpResponseRedirect(reverse(question_view, args=[question.pk]))
            except ValueError:
                pass
    else:
        form = QuestionForm()
    
    return render_to_response('question_form.html', locals(), context_instance=RequestContext(request))

def update_question(request, qid):
    if(request.POST):
        question = Question.objects.get(id__exact=qid)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(reverse(question_view, args=[question.pk]))
    else:
        question = Question.objects.get(id__exact=qid)
        form = QuestionForm(instance=question)
    return render_to_response('question_form.html', locals(), context_instance=RequestContext(request))

def delete_question(request, qid):
    question = Question.objects.get(id__exact=qid)
    question.delete()
    return HttpResponseRedirect('/questions')
