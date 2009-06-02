from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import permalink
from django.contrib import admin
from datetime import datetime
from django.db import models

import tagging
from tagging.fields import TagField
from tagging.models import Tag

from djangosphinx import SphinxSearch

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
        
    search = SphinxSearch(
        index ='questions_question',
        weights = {
            'question': 100,
            'tags': 80,
            'author': 40,
        }
    )
