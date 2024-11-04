from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import EmailLoginForm


class EmailLoginView(FormView):
    template_name = "account/login.html"
    form_class = EmailLoginForm
    success_url = reverse_lazy("home:home")  # specify redirect to on login successfuly.

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
