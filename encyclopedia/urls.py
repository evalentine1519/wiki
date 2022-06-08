from django.urls import include, path

from . import views

"""
Paths here are referenced to the root
"""

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random", views.random, name="random"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit")
]
