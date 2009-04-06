from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from models import Question
from forms import QuestionForm

def questions_home(request):
    return render_to_response('questions_base.html')
    
def question_view(request, qid):
    question = Question.objects.get(id__exact=qid)
    return render_to_response('question_detail.html')
        
def create_question(request):
    if(request.POST):
        form = QuestionForm(request.POST)
        try:
            form.save()
            return HttpResponseRedirect(reverse('questions.views.question_detail', args=(.id,)))
        except ValueError:
            pass
    else:
        form = QuestionForm()
        
    return render_to_response('question_form.html', locals())
    
def update_question(request, qid):
    if(request.POST):
        a = Article.objects.get(pk=1)
        f = ArticleForm(instance=a)
        f.save()
    return render_to_response('question_form.html')
    
def delete_question(request):
    # add 'delete successful' message to the context
    return render_to_response('questions_base.html')