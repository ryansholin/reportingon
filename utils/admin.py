from reportingon.utils.models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','affiliation','website','bio',)
    search_fields = ['user','affiliation','website','bio',]

admin.site.register(UserProfile, UserProfileAdmin)
