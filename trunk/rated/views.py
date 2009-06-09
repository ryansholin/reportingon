from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson

from reportingon.rated.models import Rated

@login_required
def rate(request, content_type_id, object_id):
    
    content_type = ContentType.objects.get(id__exact=content_type_id)
    
    # Prevent duplicates
    try:
        CurrentlyRated = Rated.objects.get(content_type=content_type, object_id__exact=object_id, user=request.user)
        CurrentlyRated.delete()
    except:
        rated = Rated(
            content_type = content_type,
            object_id = object_id,
            user = request.user
        )
        rated.save()
        data = {'object_id': object_id, 'state': 'rated', 'content_type_id': content_type_id}
        return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
        
    data = {'object_id': object_id, 'state': 'unrated', 'content_type_id': content_type_id}
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
