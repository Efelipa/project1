from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random_page, name="random"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("search", views.search, name="search"),
    path("edit_page/<str:title>", views.edit, name="edit_page"),
]
