from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import User

import tagging
from tagging.models import Tag
from tagging.fields import TagField

from datetime import datetime # for date defaults

class Question(models.Model):
    """Question model"""
    STATUS_CHOICES = (
        (1, _('Published')),
        (2, _('Closed')),
    )
    title           = models.CharField(_('title'), max_length=250)
    slug            = models.SlugField(_('slug'), editable=False, null=False, blank=False)
    author          = models.ForeignKey(User, blank=False, null=False)
    body            = models.TextField(_('body'), blank=False)
    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    published       = models.DateTimeField(_('publish'), default=datetime.now)
    created         = models.DateTimeField(_('created'), auto_now_add=True,)
    modified        = models.DateTimeField(_('modified'), auto_now=True)
    tags            = TagField()
    # objects         = QuestionManager()

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        db_table  = 'ro_questions'
        ordering  = ('-modified',)
        get_latest_by = 'published'
    
    # we'll use sphinx later on because it's sick    
    # search = SphinxSearch(
    #        index ='questions', 
    #        weights = { # individual field weighting
    #            'title': 100,
    #            'tags': 80,
    #            'body': 50,
    #        }
    #    )

    class Admin:
        pass

    def __unicode__(self):
        return u'%s' % self.title
           
    # once the view is created, unleash this puppy
    # @permalink 
    # def get_absolute_url(self): 
    #     return ('question_detail', None, {
    #         'slug': self.slug,
    #         })