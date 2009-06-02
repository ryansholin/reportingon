from reportingon.questions.models import Question
from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question','status','author','created',)
    ordering = ('-created',)
    prepopulated_fields = {'slug': ('question',)}
    search_fields = ['question',]
    
admin.site.register(Question, QuestionAdmin)
