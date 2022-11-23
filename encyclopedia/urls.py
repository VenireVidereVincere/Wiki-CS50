from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("edit", views.edit, name="edit"),
    path("<str:entry_title>", views.entry, name="entry")
]
