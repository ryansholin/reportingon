from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def home(request):
    assert False, 'test'
    return render_to_response('home_not_logged_in.html', locals(), context_instance=RequestContext(request))
