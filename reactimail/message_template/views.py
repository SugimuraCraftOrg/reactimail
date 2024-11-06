from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import MessageTemplate
from .forms import MessageTemplateForm


class MessageTemplateCreateView(LoginRequiredMixin, CreateView):
    model = MessageTemplate
    form_class = MessageTemplateForm
    template_name = "message_template/form.html"
    success_url = reverse_lazy("message_template:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["account"] = self.request.user  # Pass the account to the form
        return kwargs

    def form_valid(self, form):
        form.instance.account = self.request.user  # Set the account to the current user
        return super().form_valid(form)


class MessageTemplateListView(LoginRequiredMixin, ListView):
    model = MessageTemplate
    template_name = "message_template/list.html"

    def get_queryset(self):
        return MessageTemplate.objects.filter(account=self.request.user)


class MessageTemplateDetailView(LoginRequiredMixin, DetailView):
    model = MessageTemplate
    template_name = "message_template/detail.html"

    def get_queryset(self):
        return MessageTemplate.objects.filter(account=self.request.user)


class MessageTemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = MessageTemplate
    form_class = MessageTemplateForm
    template_name = "message_template/form.html"
    success_url = reverse_lazy("message_template:list")

    def get_queryset(self):
        return MessageTemplate.objects.filter(account=self.request.user)


class MessageTemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = MessageTemplate
    template_name = "message_template/confirm_delete.html"
    success_url = reverse_lazy("message_template:list")

    def get_queryset(self):
        return MessageTemplate.objects.filter(account=self.request.user)
