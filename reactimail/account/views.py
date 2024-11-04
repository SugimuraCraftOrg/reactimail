from django.contrib.auth import login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django_ratelimit.decorators import ratelimit

from .constants import LOGIN_MAX_TIMES_PER_MINUTE, SESSION_EXPIRE_SECONDS
from .forms import EmailLoginForm


@method_decorator(
    ratelimit(key="ip", rate=f"{LOGIN_MAX_TIMES_PER_MINUTE}/m", method=("POST",)),
    name="post",
)
class EmailLoginView(FormView):
    template_name = "account/login.html"
    form_class = EmailLoginForm
    success_url = reverse_lazy("home:home")  # specify redirect to on login successfuly.

    def form_valid(self, form):
        login(self.request, form.get_user())
        self.request.session.cycle_key()  # Prevent session fixation.
        self.request.session.set_expiry(SESSION_EXPIRE_SECONDS)  # Set session timeout.
        return super().form_valid(form)
