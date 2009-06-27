from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from reportingon.questions.models import Question
from tagging.models import Tag, TaggedItem
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

class LatestQuestions(Feed):
    title = "The latest questions from ReportingOn"
    link = "/questions/"
    description = "The most recent queries on topics from reporters like you"

    def items(self):
        return Question.objects.order_by('-created')[:10]
        
class LatestQuestionsByUser(Feed):
    def get_object(self, bits):     
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__iexact=bits[0])

    def title(self, obj):
        name = "%s %s" % (obj.first_name, obj.last_name)
        return "ReportingOn: The latest questions from %s%s" % (obj.username, " (%s)" % name if name is not '' else '')

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return 'users/%s' % obj.id

    def description(self, obj):
        return "The most recent questions asked by %s" % obj.username

    def items(self, obj):
       return Question.objects.filter(author=obj).order_by('-created')
        
class LatestAnswersByQuestion(Feed):
    def get_object(self, bits):        
        if len(bits) == 0 or len(bits) > 2:
            raise ObjectDoesNotExist
        return Question.objects.get(username__iexact=bits[0])

    def title(self, obj):
        return "ReportingOn: The latest answers to %s" % obj.question

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return 'questions/%s/%s' % (obj.id, obj.slug)

    def description(self, obj):
        return "The most recent answers to the question %s" % obj.question

    def items(self, obj):
       return Comment.objects.filter(object_pk__iexact=obj.id).order_by('-submit_date')
        
class LatestQuestionsBySearch(Feed):
    def get_object(self, bits):        
        return bits[0]

    def title(self, obj):
        return "ReportingOn search for %s" % obj
        
    def link(self, obj):
        return 'search/%s' % obj

    def description(self, obj):
        return "New question search results for %s" % obj

    def items(self, obj):
        raw_results = Question.search.query(obj)
        raw_count = raw_results.count()
        results = raw_results[0:raw_count if raw_count < 10 else 10]
        return results
        
class LatestQuestionsByBeat(Feed):
    def get_object(self, bits):        
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__iexact=bits[0])

    def title(self, obj):
        return "ReportingOn: The latest questions in %s" % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return 'beats/%s' % obj.name

    def description(self, obj):
        return "The most recent questions categorized in %s" % obj.name

    def items(self, obj):
       return Question.objects.filter(tags__icontains=obj.name).order_by('-created')[:10]