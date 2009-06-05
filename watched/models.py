from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

class Watched(models.Model):
    """Watched model"""
    
    STATUS_CHOICES = (
        (1, _('Active')),
        (2, _('Inactive')),
    )
    
    content_type_id = models.IntegerField(null=False)
    object_pk       = models.IntegerField(null=False)
    user            = models.ForeignKey(User, null=False)
    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now=True)
    status          = models.IntegerField(choices=STATUS_CHOICES, default=1, blank=True, null=False)

    class Meta:
        verbose_name = _('Watched item')
        verbose_name_plural = _('Watched items')
        ordering  = ('-created',)
    
    def content_object(self):
        content_type = ContentType.objects.get(id=self.content_type_id)
        content_object = content_type.get_object_for_this_type(id=self.object_pk)
        content_object.content_type = content_type
        return content_object
    
    def __unicode__(self):
        return u'%s' % (self.get_content_object())

class SavedSearch(models.Model):
    """Saved Search model"""    
    
    query = models.TextField()
    
    class Meta:
        verbose_name = _('Saved search')
        verbose_name_plural = _('Saved searches')
    
    def get_absolute_url(self):
        return "/search/%s" % self.query
    
    def __unicode__(self):
        return u'%s' % self.query
