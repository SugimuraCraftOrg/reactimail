from django.urls import path
from . import views

app_name = "tag"

urlpatterns = [
    path("", views.TagListView.as_view(), name="list"),
    path("add/", views.TagCreateView.as_view(), name="add"),
    path("<uuid:pk>/", views.TagDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", views.TagUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete/", views.TagDeleteView.as_view(), name="delete"),
]
