from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from reportingon.watched.models import Watched

@login_required
def watch(request, content_type_id, object_pk):
    
    # Prevent duplicates
    try:
        CurrentlyWatched = Watched.objects.get(content_type_id__exact=content_type_id, object_pk__exact=object_pk, user=request.user)
    except:
        watched = Watched(
            content_type_id = content_type_id,
            object_pk = object_pk,
            user = request.user
        )
        watched.save()
    
    return HttpResponse('')
