from reportingon.questions.models import Question
from reportingon.watched.models import Watched, SavedSearch
from django.contrib.comments.models import Comment

# requires 'user' object
def get_recent_activity_for_user(user, sort=False, thirdPerson=False):
    user_url = '/users/%s' % user.username
    recent_activity = list()
    for obj in Watched.objects.filter(user=user):
        if obj.content_type.model == 'user': # user is watching a user
            description = """%s watching <a href="#">%s</a>""" % ("""<a href="%s">%s</a> started""" % (user_url, user.username) if thirdPerson else 'Started', obj.object.username)
        elif obj.content_type.model == 'tag':
            tag_url = '/tags/%s' % obj.object.name
            description = """%s watching the &ldquo;<a href="#">%s</a>&rdquo; beat""" % ("""<a href="%s">%s</a> started""" % (tag_url, user.username) if thirdPerson else 'Started', obj.object.name)
        elif obj.content_type.model == 'question':
            question_url = '/questions/%s/%s' % (obj.object.id, obj.object.slug)
            description = """%s watching the question &ldquo;<a href="#">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> started""" % (question_url, user.username) if thirdPerson else 'Started', obj.object.question)
        elif obj.content_type.model == 'savedsearch':
            # search_url = '/?'
            description = """%s watching the search &ldquo;<a href="#">%s</a>&rdquo;""" % ("""<a href="#">%s</a> started""" % user.username if thirdPerson else 'Started', obj.object.query)
        else:
            continue
        recent_activity.append({ 'description': description, 'date': obj.created })
        description = ''
        
    for obj in Question.objects.filter(author=user):
        recent_activity.append({ 'description': """%s &ldquo;<a href="#">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> asked""" % (user_url, user.username) if thirdPerson else 'Asked', obj.question), 'date': obj.created })
    
    for obj in Comment.objects.filter(user=user):
        try:
            question = Question.objects.get(id=obj.object_pk)
            question_url = '/questions/%s/%s' % (question.id, question.slug)
            recent_activity.append({ 'description': """%s a <a href="%s">question</a> with &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> answered""" % (user_url, user.username) if thirdPerson else 'Answered', question_url, question_url, obj.comment), 'date': obj.submit_date })
        except:
            pass
    
    if sort:
        recent_activity.sort(key=lambda x:x['date'], reverse=True)
    
    return recent_activity
    
# requires a 'question' object
def get_recent_activity_for_question(question, sort=False, thirdPerson=False):
    """
        single question has a creation date, date_updated, and answers to that question
    """
    recent_activity = list()
    
    # add original question asking
    user_url = "/users/%s" % question.author.username
    question_url = '/questions/%s/%s' % (question.id, question.slug)
    recent_activity.append({ 'description': """<a href="%s">%s</a> asked &ldquo;<a href="%s">%s</a>&rdquo;""" % (user_url, question.author.username, question_url, question.question), 'date': question.created })
    
    # add update if created != modified
    if(question.created is not question.modified):
        recent_activity.append({ 'description': """<a href="%s">%s</a> updated a question &ldquo;<a href="%s">%s</a>&rdquo;""" % (user_url, question.author.username, question_url, question.question), 'date': question.modified })
        
    for answer in Comment.objects.filter(object_pk=question.id):
        if answer.user_id:
            recent_activity.append({ 'description': """<a href="#">%s</a> posted an answer to &ldquo;<a href="#">%s</a>&rdquo;""" % (answer.user.username, question.question), 'date': answer.submit_date })
            
    if sort:
        recent_activity.sort(key=lambda x:x['date'], reverse=True)
        
    return recent_activity