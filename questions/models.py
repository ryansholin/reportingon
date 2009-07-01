from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

from django.contrib.contenttypes.models import ContentType

import tagging
from tagging.fields import TagField
from tagging.models import Tag

from djangosphinx import SphinxSearch

from reportingon.rated.models import Rated

from django.contrib.comments.models import Comment

from django.contrib.comments import signals
from reportingon.signals import *

class Question(models.Model):
    """Question model"""
    
    STATUS_CHOICES = (
        (1, _('Open')),
        (2, _('Closed')),
    )
    
    question    = models.TextField(_('question'))
    slug        = models.SlugField(_('slug'), null=False, blank=True)
    author      = models.ForeignKey(User, blank=True, null=False)
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1, blank=True)
    created     = models.DateTimeField(_('created'), auto_now_add=True)
    modified    = models.DateTimeField(_('modified'), auto_now=True)
    tags        = TagField(blank=False)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering  = ('-created',)

    def __unicode__(self):
        return u'%s' % self.question
    
    def get_absolute_url(self):
        return "/questions/%d/%s" % (self.id, self.slug)
        
    signals.comment_was_posted.connect(question_has_new_answer, sender=Comment)
    
    search = SphinxSearch(
        index ='questions_question',
        weights = {
            'question': 100,
            'tags': 80,
            'author': 40,
        }
    )
    
    def get_score(self):
        answer_content_type = ContentType.objects.get(name='comment')
        question_content_type = ContentType.objects.get(name='question')
        
        answers = Comment.objects.filter(content_type=question_content_type.id, object_pk=self.id)
        question_points = 0
        answer_points = 0
        
        for answer in answers:
            answer_points += Rated.objects.filter(content_type=answer_content_type.id, object_id=answer.id).count()
        
        question_points = Rated.objects.filter(content_type=question_content_type.id, object_id=self.id).count()
        
        return answers.count() + question_points + answer_points
