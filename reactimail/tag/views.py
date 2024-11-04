from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import TagForm
from .models import Tag


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "tag/list.html"

    def get_queryset(self):
        # Filter tags by the logged-in user
        return Tag.objects.filter(account=self.request.user)


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = "tag/detail.html"

    def get_queryset(self):
        # Ensure only tags belonging to the user can be edited
        return Tag.objects.filter(account=self.request.user)


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tag/form.html"
    success_url = reverse_lazy("tag:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["account"] = self.request.user  # Pass the account to the form
        return kwargs

    def form_valid(self, form):
        form.instance.account = self.request.user  # Set the account to the current user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Optionally handle additional logging or processing here if needed
        return super().form_invalid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tag/form.html"
    success_url = reverse_lazy("tag:list")

    def get_queryset(self):
        # Ensure only tags belonging to the user can be edited
        return Tag.objects.filter(account=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["account"] = self.request.user  # Pass the account to the form
        return kwargs

    def form_valid(self, form):
        form.instance.account = self.request.user  # Set the account to the current user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Optionally handle additional logging or processing here if needed
        return super().form_invalid(form)


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "tag/confirm_delete.html"
    success_url = reverse_lazy("tag:list")

    def get_queryset(self):
        # Ensure only tags belonging to the user can be deleted
        return Tag.objects.filter(account=self.request.user)
