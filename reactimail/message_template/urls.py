from django.urls import path
from . import views

app_name = "message_template"

urlpatterns = [
    path("add/", views.MessageTemplateCreateView.as_view(), name="add"),
    path("", views.MessageTemplateListView.as_view(), name="list"),
    path("<uuid:pk>/", views.MessageTemplateDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", views.MessageTemplateUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete/", views.MessageTemplateDeleteView.as_view(), name="delete"),
]
