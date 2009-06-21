from django.template import Library
from django.utils.safestring import mark_safe
import re

register = Library()

@register.filter(name='at_reply')
def at_reply(tweet):
    pattern = re.compile(r"(\A|\W)@(?P<user>\w+)(\Z|\W)")
    repl = (r'\1@<a href="/users/\g<user>"'
    r' title="\g<user>\' profile">\g<user></a>\3')
	
    return mark_safe(pattern.sub(repl, tweet))