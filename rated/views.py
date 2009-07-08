from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from reportingon.rated.models import Rated

@login_required
def rate(request, content_type_id, object_id, rated_user_id):
    
    rated_user = User.objects.get(id__exact=rated_user_id)
    
    # Prevent users from voting on their own items
    if request.user = rated_user:
        data = {'object_id': object_id, 'state': 'unrated', 'content_type_id': content_type_id}
        return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
    
    content_type = ContentType.objects.get(id__exact=content_type_id)
    
    # Prevent duplicates
    try:
        CurrentlyRated = Rated.objects.get(content_type=content_type, object_id__exact=object_id, user=request.user)
        CurrentlyRated.delete()
    except:
        rated = Rated(
            content_type = content_type,
            object_id = object_id,
            user = request.user,
            rated_user = rated_user
        )
        rated.save()
        data = {'object_id': object_id, 'state': 'rated', 'content_type_id': content_type_id}
        
        if 'HTTP_REFERER' in request.META:
            if 'user/signin' in request.META['HTTP_REFERER']:
                # User has just logged in, return to object.
                return HttpResponseRedirect(rated.object.get_absolute_url())
        
        return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
        
    data = {'object_id': object_id, 'state': 'unrated', 'content_type_id': content_type_id}
    
    if 'HTTP_REFERER' in request.META:
        if 'user/signin' in request.META['HTTP_REFERER']:
            # User has just logged in, return to object.
            return HttpResponseRedirect(CurrentlyRated.object.get_absolute_url())
    
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
