from django.contrib.contenttypes.models import ContentType
from django import template

from reportingon.watched.models import Watched
from reportingon.rated.models import Rated
 
register = template.Library()

class WatchedNode(template.Node):
    def __init__(self, object, user, varname):
        self.varname = varname
        self.object = template.Variable(object)
        self.user = template.Variable(user)

    def render(self, context):
        try:
            Watched.objects.get(content_type=ContentType.objects.get_for_model(self.object.resolve(context)),
                                object_id=self.object.resolve(context).id,
                                user=self.user.resolve(context),
                                status=1)
            context[self.varname] = True
        except:
            context[self.varname] = False
        return ''

@register.tag(name="watched")
def watched(parser, token):
    bits = token.contents.split()
    return WatchedNode(bits[1], bits[2], bits[4])

class RatedNode(template.Node):
    def __init__(self, object, user, varname):
        self.varname = varname
        self.object = template.Variable(object)
        self.user = template.Variable(user)

    def render(self, context):
        try:
            Rated.objects.get(content_type=ContentType.objects.get_for_model(self.object.resolve(context)),
                              object_id=self.object.resolve(context).id,
                              user=self.user.resolve(context))
            context[self.varname] = True
        except:
            context[self.varname] = False
        return ''

@register.tag(name="rated")
def rated(parser, token):
    bits = token.contents.split()
    return RatedNode(bits[1], bits[2], bits[4])
