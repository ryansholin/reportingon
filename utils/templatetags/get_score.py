from django.contrib.contenttypes.models import ContentType
from django import template

from reportingon.rated.models import Rated
 
register = template.Library()

class GetScoreNode(template.Node):
    def __init__(self, object):
        self.object = template.Variable(object)

    def render(self, context):
        return Rated.objects.filter(content_type=ContentType.objects.get_for_model(self.object.resolve(context)), object_id=self.object.resolve(context).id).count()

@register.tag(name="get_score")
def get_score(parser, token):
    bits = token.contents.split()
    return GetScoreNode(bits[1])
