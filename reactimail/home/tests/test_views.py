import pytest
from django.urls import reverse

from account.tests.factories import UserFactory


class TestHome:
    @pytest.mark.django_db
    def test_home_authenticated(self, client):
        """Should be displayed email when logged in."""
        UserFactory(email="testuser@example.com", password="testpassword")

        client.login(email="testuser@example.com", password="testpassword")
        response = client.get(reverse("home:home"))

        assert response.status_code == 200
        assert "testuser@example.com" in response.content.decode()

    @pytest.mark.django_db
    def test_home_unauthenticated(self, client):
        """Should be displayed login screen when not logged out.

        - The home URL should also be specified for when the user logs in again.
        """
        response = client.get(reverse("home:home"))

        assert response.status_code == 302
        assert response.url == reverse("account:login") + "?next=" + reverse(
            "home:home"
        )
