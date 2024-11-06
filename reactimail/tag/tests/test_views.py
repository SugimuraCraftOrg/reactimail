import pytest
from django.urls import reverse

from account.tests.factories import AccountFactory
from tag.models import Tag
from .factories import TagFactory


@pytest.mark.django_db
class TestTagAdd:
    @pytest.fixture
    def target(self):
        return reverse("tag:add")

    def test_success(self, target, client):
        """Should add tag successfully."""
        from tag.models import Tag

        account = AccountFactory()

        client.force_login(account)
        response = client.post(
            target,
            {
                "name": "New Tag",
            },
        )

        assert (
            response.status_code == 302
        )  # Check for redirect after successful creation
        assert Tag.objects.count() == 1
        assert Tag.objects.first().name == "New Tag"

    def test_failure_by_same_name(self, target, client):
        """Should not add tag."""
        from tag.models import Tag

        account = AccountFactory()
        TagFactory(account=account, name="Tag Name")

        client.force_login(account)
        response = client.post(
            target,
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
    @pytest.fixture
    def target(self):
        return reverse("tag:list")

    def test_no_tags(self, target, client):
        """Should display message for no data."""
        account = AccountFactory()

        client.force_login(account)
        response = client.get(target)

        assert response.status_code == 200
        assert "No tags found." in response.content.decode()

    def test_display_all_tags(self, target, client):
        """Should display 5 data."""
        account = AccountFactory()
        TagFactory.create_batch(5, account=account)

        client.force_login(account)
        response = client.get(target)

        assert response.status_code == 200
        assert len(response.context["object_list"]) == 5

    def test_does_not_display_other_users_tags(self, target, client):
        """Should not display other's data."""
        account = AccountFactory()
        TagFactory.create_batch(5, account=account)
        other_account = AccountFactory()
        TagFactory.create_batch(3, account=other_account)  # Other user's tags

        client.force_login(account)
        response = client.get(target)

        assert response.status_code == 200
        assert len(response.context["object_list"]) == 5


@pytest.mark.django_db
class TestTagDetail:
    @pytest.fixture
    def target(self):
        def _method(tag: Tag):
            return reverse("tag:detail", args=[tag.id])

        return _method

    def test_display_tags(self, target, client):
        """Should display data."""
        account = AccountFactory()
        tag = TagFactory(account=account)

        client.force_login(account)
        response = client.get(target(tag))

        assert response.status_code == 200
        assert response.context["object"].id == tag.id

    def test_does_not_display_other_users_tag(self, target, client):
        """Should not display other's data."""
        account = AccountFactory()
        other_account = AccountFactory()
        other_tag = TagFactory(account=other_account)

        client.force_login(account)
        response = client.get(target(other_tag))

        assert response.status_code == 404


@pytest.mark.django_db
class TestTagUpdate:
    @pytest.fixture
    def target(self):
        def _method(tag: Tag):
            return reverse("tag:edit", args=[tag.id])

        return _method

    def test_update_own_tag(self, target, client):
        account = AccountFactory()
        tag = TagFactory(account=account, name="Old Tag Name")

        client.force_login(account)
        data = {"name": "Updated Tag Name"}
        response = client.post(target(tag), data)

        tag.refresh_from_db()
        assert response.status_code == 302
        assert tag.name == "Updated Tag Name"

    def test_update_with_same_name(self, target, client):
        account = AccountFactory()
        tag = TagFactory(account=account, name="Tag Name")

        client.force_login(account)
        data = {"name": "Tag Name"}
        response = client.post(target(tag), data)

        tag.refresh_from_db()
        assert response.status_code == 302
        assert tag.name == "Tag Name"

    def test_cannot_update_other_users_tag(self, target, client):
        account = AccountFactory()
        other_account = AccountFactory()
        tag = TagFactory(account=other_account, name="Other User's Tag")

        client.force_login(account)
        data = {"name": "Attempted Update"}
        response = client.post(target(tag), data)

        tag.refresh_from_db()
        assert response.status_code == 404


@pytest.mark.django_db
class TestTagDelete:
    @pytest.fixture
    def target(self):
        def _method(tag: Tag):
            return reverse("tag:delete", args=[tag.id])

        return _method

    def test_delete_own_tag(self, target, client):
        from tag.models import Tag

        account = AccountFactory()
        tag = TagFactory(account=account)

        client.force_login(account)
        response = client.post(target(tag))

        assert response.status_code == 302
        assert not Tag.objects.filter(id=tag.id).exists()

    def test_cannot_delete_other_users_tag(self, target, client):
        from tag.models import Tag

        account = AccountFactory()
        other_account = AccountFactory()
        other_tag = TagFactory(account=other_account)

        client.force_login(account)
        response = client.post(target(other_tag))

        assert response.status_code == 404
        assert Tag.objects.filter(id=other_tag.id).exists()
