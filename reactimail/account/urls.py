from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import EmailLoginView

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="account:login"), name="logout"),
]
