from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from reportingon.watched.models import Watched, SavedSearch

@login_required
def watch(request, content_type_id, object_id):
    
    content_type = ContentType.objects.get(id__exact=content_type_id)
    
    # Prevent duplicates
    try:
        CurrentlyWatched = Watched.objects.get(content_type=content_type, object_id__exact=object_id, user=request.user)
    except:
        watched = Watched(
            content_type = content_type,
            object_id = object_id,
            user = request.user
        )
        watched.save()
        return HttpResponse('OK')
    return HttpResponse('OK - duplicate')

@login_required
def save_search(request, query):
    try:
        CurrentlySavedSearch = SavedSearch.objects.get(query__exact=query)
    except:
        saved_search = SavedSearch(query = query)
        saved_search.save()
        return watch(request, ContentType.objects.get_for_model(SavedSearch).pk, saved_search.pk)
    return watch(request, ContentType.objects.get_for_model(SavedSearch).pk, CurrentlySavedSearch.pk)
