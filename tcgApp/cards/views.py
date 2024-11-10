from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Card, Collection

@login_required(login_url="/users/login/")
def IndexView(request):
    latest_collection_list = Collection.objects.order_by("-pub_date")[:5]
    return render(request, 'cards/index.html', {'latest_collection_list': latest_collection_list})


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/users/login/"
    redirect_field_name = 'redirect_to'
    model = Collection
    template_name = "cards/detail.html"

    def get_queryset(self):
        """
        Excludes any collections that aren't published yet.
        """
        return Collection.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoginRequiredMixin, generic.DetailView):
    login_url = "/users/login/"
    redirect_field_name = 'redirect_to'
    model = Collection
    template_name = "cards/results.html"

@login_required(login_url="/users/login/")
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