from django.urls import path
from .views import *

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("search", Search.as_view(), name="search"),
    path("list", List.as_view(), name="list"),
    path("details/<int:mov_exid>", Details.as_view(), name="details"),
    path("besave", BackendSave.as_view(), name="backendsave")
]