from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import permalink
from django.contrib import admin
from datetime import datetime
from django.db import models

import tagging
from tagging.fields import TagField
from tagging.models import Tag

class Question(models.Model):
    """Question model"""
    
    STATUS_CHOICES = (
        (1, _('Open')),
        (2, _('Closed')),
    )
    
    question    = models.TextField(_('question'))
    slug        = models.SlugField(_('slug'), editable=False, null=False, blank=False)
    author      = models.ForeignKey(User, blank=False, null=False)
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    created     = models.DateTimeField(_('created'), auto_now_add=True)
    modified    = models.DateTimeField(_('modified'), auto_now=True)
    tags        = TagField()

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering  = ('-created',)

    def __unicode__(self):
        return u'%s' % self.question
    
    @permalink 
    def get_absolute_url(self): 
        return ('question_view', None, {'slug': self.slug})
