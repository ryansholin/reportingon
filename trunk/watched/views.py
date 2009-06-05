from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from reportingon.watched.models import Watched, SavedSearch

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
        return HttpResponseRedirect(watched.content_object().get_absolute_url())
    return HttpResponseRedirect(CurrentlyWatched.content_object().get_absolute_url())

@login_required
def save_search(request, query):
    try:
        CurrentlySavedSearch = SavedSearch.objects.get(query__exact=query)
    except:
        saved_search = SavedSearch(query = query)
        saved_search.save()
        return watch(request, ContentType.objects.get_for_model(SavedSearch).id, saved_search.pk)
    return watch(request, ContentType.objects.get_for_model(SavedSearch).id, CurrentlySavedSearch.pk)
