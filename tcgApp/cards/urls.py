from django.urls import path

from . import views

app_name = "cards"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:collection_id>/submit/", views.submit, name="submit"),
]