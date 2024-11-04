import pytest
from django.core.cache import cache
from django.urls import reverse

from .factories import AccountFactory


class TestAuth:
    @pytest.mark.django_db
    def test_login_success(self, client):
        """Should login successfully and authenticate the user."""
        AccountFactory(email="testuser@example.com", password="testpassword")
        cache.clear()  # reset ratelimit.

        response = client.post(
            reverse("account:login"),
            {
                "email": "testuser@example.com",
                "password": "testpassword",
            },
        )

        assert response.status_code == 302  # should be redirect.
        assert response.url == reverse("home:home")  # should be redirect to home.
        assert "_auth_user_id" in client.session  # verify user is authenticated.

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
        AccountFactory(email="testuser@example.com", password="testpassword")
        cache.clear()  # reset ratelimit.

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
        assert (
            "_auth_user_id" not in client.session
        )  # verify user is not authenticated.

    @pytest.mark.django_db
    def test_login_success_within_number_of_attempts(self, client):
        """Should success within the number of attempts."""
        from account.constants import LOGIN_MAX_TIMES_PER_MINUTE

        AccountFactory(email="testuser@example.com", password="testpassword")
        cache.clear()  # reset ratelimit.

        url = reverse("account:login")
        login_data = {"email": "testuser@example.com", "password": "incorrectpassword"}

        # Let fail up to one time before the limit.
        for _ in range(LOGIN_MAX_TIMES_PER_MINUTE - 1):
            response = client.post(url, login_data)
            assert response.status_code == 200
            assert "Email or password is incorrect" in response.content.decode()

        # Success with a limited number of times.
        login_data["password"] = "testpassword"
        response = client.post(url, login_data)

        assert response.status_code == 302
        assert response.url == reverse("home:home")

    @pytest.mark.django_db
    def test_login_failure_with_over_attempts(self, client):
        """Should failure of more than the number of attempts."""
        from account.constants import LOGIN_MAX_TIMES_PER_MINUTE

        AccountFactory(email="testuser@example.com", password="testpassword")
        cache.clear()  # reset ratelimit.

        url = reverse("account:login")
        login_data = {"email": "testuser@example.com", "password": "incorrectpassword"}

        # Let fail up to the limit.
        for _ in range(LOGIN_MAX_TIMES_PER_MINUTE):
            response = client.post(url, login_data)
            assert response.status_code == 200
            assert "Email or password is incorrect" in response.content.decode()

        # Will failure due to requests exceeding the limit.
        login_data["password"] = "testpassword"
        response = client.post(url, login_data)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_session_expiry(self, client):
        from django.utils import timezone
        from freezegun import freeze_time

        from account.constants import SESSION_EXPIRE_SECONDS

        AccountFactory(email="testuser@example.com", password="testpassword")
        cache.clear()  # reset ratelimit.

        login_url = reverse("account:login")
        login_data = {"email": "testuser@example.com", "password": "testpassword"}
        response = client.post(login_url, login_data)

        # Set the current time as a future date.
        with freeze_time(
            timezone.now() + timezone.timedelta(seconds=SESSION_EXPIRE_SECONDS + 1)
        ):
            home_url = reverse("home:home")
            response = client.get(home_url)
            assert response.status_code == 302
            assert reverse("account:login") in response.url  # redirect to login form.
