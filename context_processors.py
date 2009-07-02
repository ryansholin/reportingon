from utils.activity import *

from reportingon.questions.models import Question
from tagging.models import Tag

def global_resources(request):
    try:
        user_score = get_user_score_for_user(request.user)
    except:
        user_score = 'N/A'
    
    popular_beats = Tag.objects.usage_for_model(Question, counts=True)
    popular_beats.sort(key=lambda x: x.count, reverse=True)
    popular_beats = popular_beats[:5]
    
    latest_questions = Question.objects.order_by('-created')[:5]
        
    return locals()
