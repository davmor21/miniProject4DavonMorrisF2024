from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Card, Collection

class IndexView(generic.ListView):
    template_name = "cards/index.html"
    context_object_name = "latest_collection_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Collection.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
               :5
               ]

class DetailView(generic.DetailView):
    model = Collection
    template_name = "cards/detail.html"

    def get_queryset(self):
        """
        Excludes any collections that aren't published yet.
        """
        return Collection.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Collection
    template_name = "cards/results.html"


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