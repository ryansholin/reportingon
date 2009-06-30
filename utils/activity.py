from reportingon.questions.models import Question
from reportingon.watched.models import Watched, SavedSearch
from django.contrib.comments.models import Comment

# requires 'user' object
def get_recent_activity_for_user(user, sort=False, thirdPerson=False, unique=False):
    recent_activity = list()
    watched_beats = list(Watched.objects.filter(user=user, content_type__model='tag'))
    watched_questions = list(Watched.objects.filter(user=user, content_type__model='question'))
    for obj in Watched.objects.filter(user=user):
        if obj.content_type.model == 'user': # user is watching a user
            type = 'user-watched-user'
            description = """%s watching <a href="%s">%s</a>""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', obj.object.get_absolute_url(), obj.object.username)
        elif obj.content_type.model == 'tag':
            type = 'user-watched-beat'
            tag_url = '/beats/%s' % obj.object.name
            description = """%s watching the &ldquo;<a href="%s">%s</a>&rdquo; beat""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', tag_url, obj.object.name)
                        
            # get questions for watched beat
            if obj in watched_beats: 
                questions = Question.objects.filter(tags__icontains=obj.object.name)[:50] # limit this to something reasonable...
                watched_beats.remove(obj)
                for question in questions:
                    recent_activity.append({ 'description': 'no-profile', 'date': question.created , 'type': 'question', 'id': type + str(obj.object_id), 'question': question })
            
        elif obj.content_type.model == 'question':
            type = 'user-watched-question'
            description = """%s watching the question &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', obj.object.get_absolute_url(), obj.object.question)
        elif obj.content_type.model == 'savedsearch':
            type = 'user-watched-search'
            search_url = '/search?query=' + obj.object.query
            description = """%s watching the search &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> started""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Started', search_url, obj.object.query)
        else:
            type = 'fail'
            watched_user = False
            continue
            
        recent_activity.append({ 'description': description, 'date': obj.created , 'type': type, 'id': type + str(obj.object_id), 'watched_user': user })
        description = ''
        
    for obj in Question.objects.filter(author=user):
        type = 'question'
        recent_activity.append({ 'description': """%s &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> asked""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Asked', obj.get_absolute_url(), obj.question), 'date': obj.created, 'type': type, 'question': obj, 'id': type + str(obj.id), 'watched_user': user })
    
    for obj in Comment.objects.filter(user=user):
        type = 'answer'
        try:
            question = Question.objects.get(id=obj.object_pk)
            recent_activity.append({ 'description': """%s a <a href="%s">question</a> with &ldquo;<a href="%s">%s</a>&rdquo;""" % ("""<a href="%s">%s</a> answered""" % (user.get_absolute_url(), user.username) if thirdPerson else 'Answered', question.get_absolute_url(), question.get_absolute_url() + '#answer-' + str(obj.id), obj.comment), 'date': obj.submit_date, 'type': type, 'id': type + str(question.id), 'watched_user': user, 'answer': obj, 'question': question })
        except:
            pass
        
    if unique:
        recent_activity = uniqueify(recent_activity, lambda x:x['id'])
        
    if sort:    
        recent_activity.sort(key=lambda x:x['date'], reverse=True)

    return recent_activity
    
# requires a 'question' object
def get_recent_activity_for_question(question, sort=False, thirdPerson=False, unique=False):
    """
    single question has a creation date, date_updated, and answers to that question
    """
    recent_activity = list()
    
    # add original question asking
    type = 'question'
    recent_activity.append({ 'description': """<a href="%s">%s</a> asked &ldquo;<a href="%s">%s</a>&rdquo;""" % (question.author.get_absolute_url(), question.author.username, question.get_absolute_url(), question.question), 'date': question.created, 'type': type, 'id': type + str(question.id),'watched_user': question.author, 'question': question })
    
    # add update if created != modified
    type = 'user-updated-question'
    if(question.created is not question.modified):
        recent_activity.append({ 'description': """<a href="%s">%s</a> updated a question &ldquo;<a href="%s">%s</a>&rdquo;""" % (question.author.get_absolute_url(), question.author.username, question.get_absolute_url(), question.question), 'date': question.modified, 'type': type, 'id': type + str(question.id),'watched_user': question.author })
        
    for answer in Comment.objects.filter(object_pk=question.id):
        if answer.user_id:
            type = 'answer'
            recent_activity.append({ 'description': """<a href="%s">%s</a> posted an answer to &ldquo;<a href="%s">%s</a>&rdquo;""" % (answer.user.get_absolute_url(), answer.user.username, question.get_absolute_url() + '#answer-' + str(answer.id), question.question), 'date': answer.submit_date, 'type': type, 'id': type + str(question.id),'watched_user': answer.user, 'answer': answer, 'question': question })
            
    if unique:
        recent_activity = uniqueify(recent_activity, lambda x:x['id'])
    
    if sort:
        recent_activity.sort(key=lambda x:x['date'], reverse=True)
        
    return recent_activity
    
def uniqueify(seq, idfun=None):  
    if idfun is None: 
        def idfun(x): return x 
    seen = {} 
    result = [] 
    for item in seq: 
        marker = idfun(item) 
        # in old Python versions: 
        # if seen.has_key(marker) 
        # but in new ones: 
        if marker in seen: continue 
        seen[marker] = 1 
        result.append(item) 
    return result