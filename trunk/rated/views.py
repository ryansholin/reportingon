from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from reportingon.rated.models import Rated

@login_required
def rate(request, content_type_id, object_id):
    
    content_type = ContentType.objects.get(id__exact=content_type_id)
    
    # Prevent duplicates
    try:
        CurrentlyRated = Rated.objects.get(content_type=content_type, object_id__exact=object_id, user=request.user)
    except:
        rated = Rated(
            content_type = content_type,
            object_id = object_id,
            user = request.user
        )
        rated.save()
        return HttpResponse('OK')
    return HttpResponse('OK - duplicate')
