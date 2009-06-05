from django.contrib.contenttypes.models import ContentType
from django.template import Library

register = Library()
 
@register.simple_tag
def get_content_type_id(content_type):
    return ContentType.objects.get_for_model(content_type).id
