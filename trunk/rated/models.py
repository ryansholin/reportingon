from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db import models

class Rated(models.Model):
    """Rated model"""
    
    content_type    = models.ForeignKey(ContentType, null=False)
    object_id       = models.PositiveIntegerField(null=False)
    object          = generic.GenericForeignKey('content_type', 'object_id')
    user            = models.ForeignKey(User, null=False)
    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rated item'
        verbose_name_plural = 'Rated items'
        ordering  = ('-created',)
        unique_together = (('user', 'content_type', 'object_id'),)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.object)
