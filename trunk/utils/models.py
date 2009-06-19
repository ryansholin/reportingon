from django.db import models
from django.contrib.auth.models import User

from reportingon.rated.models import Rated

from django.contrib.auth.models import User
from django.db.models import signals

class UserProfile(models.Model):
    user        = models.ForeignKey(User, unique=True)
    affiliation = models.CharField(max_length=200, blank=True)
    website     = models.URLField(blank=True)
    bio         = models.TextField(blank=True)
    
    def get_score(self):
        return Rated.objects.filter(rated_user=self.user).count()

def user_post_save(sender, instance, **kwargs):
    profile, new = UserProfile.objects.get_or_create(user=instance)

signals.post_save.connect(user_post_save, sender=User)
