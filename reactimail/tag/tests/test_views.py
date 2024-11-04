import pytest
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

    def test_failure_by_same_name(self, client):
        """Should not add tag."""
        from tag.models import Tag

        account = AccountFactory()
        TagFactory(account=account, name="Tag Name")

        client.force_login(account)
        response = client.post(
            reverse("tag:add"),
            {
                "name": "Tag Name",
            },
        )

        assert response.status_code == 200
        assert (
            "A tag with this name already exists for your account."
            in response.content.decode()
        )
        assert Tag.objects.count() == 1


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
class TestTagDetail:
    def test_no_tags(self, client):
        """Should not display data."""
        from uuid import uuid4

        account = AccountFactory()
        dummy_id = uuid4()

        client.force_login(account)
        response = client.get(reverse("tag:detail", args=[dummy_id]))

        assert response.status_code == 404

    def test_display_tags(self, client):
        """Should display data."""
        account = AccountFactory()
        tag = TagFactory(account=account)

        client.force_login(account)
        response = client.get(reverse("tag:detail", args=[tag.id]))

        assert response.status_code == 200
        assert tag.name in response.content.decode()

    def test_does_not_display_other_users_tag(self, client):
        """Should not display other's data."""
        account = AccountFactory()
        other_account = AccountFactory()
        other_tag = TagFactory(account=other_account)

        client.force_login(account)
        response = client.get(reverse("tag:detail", args=[other_tag.id]))

        assert response.status_code == 404


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

    def test_update_with_same_name(self, client):
        account = AccountFactory()
        tag = TagFactory(account=account, name="Tag Name")

        client.force_login(account)
        response = client.post(reverse("tag:edit", args=[tag.id]), {"name": "Tag Name"})

        tag.refresh_from_db()
        assert response.status_code == 302
        assert tag.name == "Tag Name"

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
