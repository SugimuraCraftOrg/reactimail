import pytest
from django.urls import reverse

from .factories import UserFactory


class TestAuth:
    @pytest.mark.django_db
    def test_login_success(self, client):
        """Should be login successfuly."""
        UserFactory(email="testuser@example.com", password="testpassword")

        response = client.post(
            reverse("account:login"),
            {
                "email": "testuser@example.com",
                "password": "testpassword",
            },
        )

        assert response.status_code == 302  # should be redirect.
        assert response.url == reverse("home:home")  # should be redirect to home.

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "email, password, description",
        [
            ("", "", "form empty"),
            ("invalid@example.com", "testpassword", "invalid email"),
            ("testuser@example.com", "wrongpassword", "invalid password"),
        ],
    )
    def test_login_fail(self, client, email, password, description):
        """Should be login failure with error messeage."""
        UserFactory(email="testuser@example.com", password="testpassword")

        response = client.post(
            reverse("account:login"),
            {
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 200  # should be ok.
        assert (
            "Email or password is incorrect" in response.content.decode()
        ), description
