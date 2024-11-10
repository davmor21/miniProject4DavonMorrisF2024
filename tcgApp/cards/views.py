from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Card, Collection

def index(request):
    latest_collection_list = Collection.objects.order_by("-pub_date")[:5]
    context = {"latest_collection_list": latest_collection_list}
    return render(request, "cards/index.html", context)

def detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    return render(request, "cards/detail.html", {"collection": collection})


def results(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    return render(request, "cards/results.html", {"collection": collection})


def submit(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    try:
        selected_card = collection.card_set.get(pk=request.POST["card"])
    except (KeyError, Card.DoesNotExist):
        # Redisplay the collection submission form.
        return render(
            request,
            "cards/detail.html",
            {
                "collection": collection,
                "error_message": "You didn't select a card.",
            },
        )
    else:
        selected_card.quantity = F("quantity") + 1
        selected_card.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("cards:results", args=(collection.id,)))