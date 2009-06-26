from reportingon.questions.models import Question
from reportingon.watched.models import Watched, SavedSearch
from django.contrib.comments.models import Comment

# requires 'user' object
def get_recent_activity_for_user(user, sort=False, thirdPerson=False):
    recent_activity = list()
    for obj in Watched.objects.filter(user=user):
        if obj.content_type.model == 'user': # user is watching a user
            type = 'user-watched-user'
            description = """%s watching <a href="%s">%s</a>""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', obj.object.get_absolute_url(), obj.object.username)
        elif obj.content_type.model == 'tag':
            type = 'user-watched-beat'
            tag_url = '/beats/%s' % obj.object.name
            description = """%s watching the &ldquo;<a href="%s">%s</a>&rdquo; beat""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', tag_url, obj.object.name)
        elif obj.content_type.model == 'question':
            type = 'user-watched-question'
            description = """%s watching the question &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', obj.object.get_absolute_url(), obj.object.question)
        elif obj.content_type.model == 'savedsearch':
            type = 'user-watched-search'
            search_url = '/search?query=' + obj.object.query
            description = """%s watching the search &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', search_url, obj.object.query)
        else:
            type = 'fail'
            continue
        recent_activity.append({ 'description': description, 'date': obj.created , 'type': type})
        description = ''
        
    for obj in Question.objects.filter(author=user):
        type = 'question'
        recent_activity.append({ 'description': """%s &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> asked""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Asked', obj.get_absolute_url(), obj.question), 'date': obj.created, 'type': type, 'question': obj })
    
    for obj in Comment.objects.filter(user=user):
        type = 'answer'
        try:
            question = Question.objects.get(id=obj.object_pk)
            recent_activity.append({ 'description': """%s a <a href="%s">question</a> with &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> answered""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Answered', question.get_absolute_url(), question.get_absolute_url() + '#answer-' + str(obj.id), obj.comment), 'date': obj.submit_date, 'type': type })
        except:
            pass
    
    return recent_activity
    
# requires a 'question' object
def get_recent_activity_for_question(question, sort=False, thirdPerson=False):
    """
    single question has a creation date, date_updated, and answers to that question
    """
    recent_activity = list()
    
    # add original question asking
    type = 'user-asked-question'
    recent_activity.append({ 'description': """<a href="%s">%s</a> asked &ldquo;<a href="%s">%s</a>&rdquo;""" % (question.author.get_absolute_url(), question.author.username, question.get_absolute_url(), question.question), 'date': question.created, 'type': type })
    
    # add update if created != modified
    type = 'user-updated-question'
    if(question.created is not question.modified):
        recent_activity.append({ 'description': """<a href="%s">%s</a> updated a question &ldquo;<a href="%s">%s</a>&rdquo;""" % (question.author.get_absolute_url(), question.author.username, question.get_absolute_url(), question.question), 'date': question.modified, 'type': type })
        
    for answer in Comment.objects.filter(object_pk=question.id):
        if answer.user_id:
            type = 'user-answered-question'
            recent_activity.append({ 'description': """<a href="%s">%s</a> posted an answer to &ldquo;<a href="%s">%s</a>&rdquo;""" % (answer.user.get_absolute_url(), answer.user.username, question.get_absolute_url() + '#answer-' + str(answer.id), question.question), 'date': answer.submit_date, 'type': type })
            
    if sort:
        recent_activity.sort(key=lambda x:x['date'], reverse=True)
        
    return recent_activity