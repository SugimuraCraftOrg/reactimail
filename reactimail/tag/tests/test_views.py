import pytest
from django.core.cache import cache
from django.urls import reverse

from account.tests.factories import AccountFactory
from .factories import TagFactory


@pytest.mark.django_db
class TestTagAdd:
    def test_success(self, client):
        """Should add tag successfully."""
        from tag.models import Tag

        account = AccountFactory()

        client.force_login(account)
        response = client.post(
            reverse("tag:add"),
            {
                "name": "New Tag",
            },
        )

        assert (
            response.status_code == 302
        )  # Check for redirect after successful creation
        assert Tag.objects.count() == 1
        assert Tag.objects.first().name == "New Tag"


@pytest.mark.django_db
class TestTagList:
    def test_no_tags(self, client):
        """Should display message for no data."""
        account = AccountFactory()

        client.force_login(account)
        response = client.get(reverse("tag:list"))

        assert response.status_code == 200
        assert "No tags available." in response.content.decode()

    def test_display_all_tags(self, client):
        """Should display 5 data."""
        account = AccountFactory()
        TagFactory.create_batch(5, account=account)

        client.force_login(account)
        response = client.get(reverse("tag:list"))

        assert response.status_code == 200
        assert len(response.context["object_list"]) == 5

    def test_does_not_display_other_users_tags(self, client):
        """Should not display other's data."""
        account = AccountFactory()
        TagFactory.create_batch(5, account=account)
        other_account = AccountFactory()
        TagFactory.create_batch(3, account=other_account)  # Other user's tags

        client.force_login(account)
        response = client.get(reverse("tag:list"))

        assert response.status_code == 200
        assert len(response.context["object_list"]) == 5


@pytest.mark.django_db
class TestTagUpdate:
    def test_update_own_tag(self, client):
        account = AccountFactory()
        tag = TagFactory(account=account, name="Old Tag Name")

        client.force_login(account)
        response = client.post(
            reverse("tag:edit", args=[tag.id]), {"name": "Updated Tag Name"}
        )

        tag.refresh_from_db()
        assert response.status_code == 302
        assert tag.name == "Updated Tag Name"

    def test_cannot_update_other_users_tag(self, client):
        account = AccountFactory()
        other_account = AccountFactory()
        tag = TagFactory(account=other_account, name="Other User's Tag")

        client.force_login(account)
        response = client.post(
            reverse("tag:edit", args=[tag.id]), {"name": "Attempted Update"}
        )

        tag.refresh_from_db()
        assert response.status_code == 404
        assert tag.name == "Other User's Tag"


@pytest.mark.django_db
class TestTagDelete:
    def test_delete_own_tag(self, client):
        from tag.models import Tag

        account = AccountFactory()
        tag = TagFactory(account=account)

        client.force_login(account)
        response = client.post(reverse("tag:delete", args=[tag.id]))

        assert response.status_code == 302
        assert not Tag.objects.filter(pk=tag.pk).exists()

    def test_cannot_delete_other_users_tag(self, client):
        from tag.models import Tag

        account = AccountFactory()
        other_account = AccountFactory()
        tag = TagFactory(account=other_account)

        client.force_login(account)
        response = client.post(reverse("tag:delete", args=[tag.id]))

        assert response.status_code == 404
        assert Tag.objects.filter(pk=tag.pk).exists()
