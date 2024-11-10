from django.urls import path

from . import views

app_name = "cards"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:collection_id>/", views.detail, name="detail"),
    path("<int:collection_id>/results/", views.results, name="results"),
    path("<int:collection_id>/submit/", views.submit, name="submit"),
]