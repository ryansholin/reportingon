from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db import models

class Watched(models.Model):
    """Watched model"""
    
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    
    content_type    = models.ForeignKey(ContentType, null=False)
    object_id       = models.PositiveIntegerField(null=False)
    object          = generic.GenericForeignKey('content_type', 'object_id')
    user            = models.ForeignKey(User, null=False)
    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now=True)
    status          = models.IntegerField(choices=STATUS_CHOICES, default=1, blank=True, null=False)

    class Meta:
        verbose_name = 'Watched item'
        verbose_name_plural = 'Watched items'
        ordering  = ('-modified',)
        
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.object)

class SavedSearch(models.Model):
    """Saved Search model"""    
    
    query = models.TextField()
    
    class Meta:
        verbose_name = 'Saved search'
        verbose_name_plural = 'Saved searches'
    
    def get_absolute_url(self):
        return "/search?query=%s" % self.query
    
    def __unicode__(self):
        return u'%s' % self.query
