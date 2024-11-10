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

    if request.method == "POST":
        # Step 1: Handle deletions
        delete_card_ids = request.POST.getlist("delete_card_ids[]")
        if delete_card_ids:
            # Delete cards that match the IDs in delete_card_ids for this collection
            Card.objects.filter(id__in=delete_card_ids, collection=collection).delete()

        # Step 2: Handle adding new cards
        new_card_names = request.POST.getlist("new_card_name[]")
        new_card_quantities = request.POST.getlist("new_card_quantity[]")
        for name, quantity in zip(new_card_names, new_card_quantities):
            if name:  # Add only if a name is provided
                Card.objects.create(
                    collection=collection,
                    card_name=name,
                    quantity=int(quantity)
                )

        # Step 3: Update quantities for existing cards
        for card in collection.card_set.all():
            quantity_field_name = f"quantity_{card.id}"
            if quantity_field_name in request.POST:
                new_quantity = request.POST.get(quantity_field_name)
                if new_quantity is not None:
                    card.quantity = int(new_quantity)
                    card.save()

        # Redirect after processing
        return HttpResponseRedirect(reverse("cards:results", args=(collection.id,)))

    return render(request, "cards/detail.html", {"collection": collection})