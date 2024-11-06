import pytest

from django.urls import reverse

from account.tests.factories import AccountFactory
from message_template.models import MessageTemplate
from .factories import MessageTemplateFactory


@pytest.mark.django_db
class TestMessageTemplateAdd:
    @pytest.fixture
    def target(self):
        return reverse("message_template:add")

    def test_message_template_add_success(self, target, client):
        account = AccountFactory()

        client.force_login(account)
        data = {
            "type": "text",
            "title": "Sample Message",
            "body": "Dear ${last_name}, welcome!",
        }
        response = client.post(target, data)

        assert response.status_code == 302  # Redirect on success
        assert MessageTemplate.objects.filter(
            title="Sample Message", account=account
        ).exists()

    def test_message_template_add_validation_error(self, target, client):
        account = AccountFactory()

        client.force_login(account)
        data = {
            "type": "text",
            "title": "",
            "body": "Invalid body ${missing_curly",
        }
        response = client.post(target, data)
        form = response.context["form"]

        assert response.status_code == 200  # Form reloads on error
        assert form.errors  # Errors present


@pytest.mark.django_db
class TestMessageTemplateList:
    @pytest.fixture
    def target(self):
        return reverse("message_template:list")

    def test_message_template_list_empty(self, target, client):
        account = AccountFactory()

        client.force_login(account)
        response = client.get(target)

        assert response.status_code == 200
        assert "No message templates found" in response.content.decode()

    def test_message_template_list_with_data(self, target, client):
        account = AccountFactory()
        MessageTemplateFactory.create_batch(5, account=account)

        client.force_login(account)
        response = client.get(target)

        assert response.status_code == 200
        assert len(response.context["object_list"]) == 5

    def test_message_template_list_excludes_other_accounts(self, target, client):
        account = AccountFactory()
        MessageTemplateFactory.create_batch(5, account=account)
        other_account = AccountFactory()
        MessageTemplateFactory.create_batch(3, account=other_account)

        client.force_login(account)
        response = client.get(target)

        assert response.status_code == 200
        assert len(response.context["object_list"]) == 5


@pytest.mark.django_db
class TestMessageTemplateDetail:
    @pytest.fixture
    def target(self):
        def _method(message_template: MessageTemplate):
            return reverse("message_template:detail", args=[message_template.id])

        return _method

    def test_message_template_detail_success(self, target, client):
        account = AccountFactory()
        message_template = MessageTemplateFactory(account=account)

        client.force_login(account)
        response = client.get(target(message_template))

        assert response.status_code == 200
        assert response.context["object"].id == message_template.id

    def test_message_template_detail_other_account(self, target, client):
        account = AccountFactory()
        other_account = AccountFactory()
        message_template = MessageTemplateFactory(account=other_account)

        client.force_login(account)
        response = client.get(target(message_template))

        assert response.status_code == 404


@pytest.mark.django_db
class TestMessageTemplateUpdate:
    @pytest.fixture
    def target(self):
        def _method(message_template: MessageTemplate):
            return reverse("message_template:edit", args=[message_template.id])

        return _method

    def test_message_template_update_success(self, target, client):
        account = AccountFactory()
        message_template = MessageTemplateFactory(
            account=account, title="Before Update"
        )

        client.force_login(account)
        data = {
            "type": "html",
            "title": "Updated Title",
            "body": "Updated Body",
        }
        response = client.post(target(message_template), data)
        message_template.refresh_from_db()

        assert response.status_code == 302
        assert message_template.title == "Updated Title"

    def test_message_template_update_validation_error(self, target, client):
        account = AccountFactory()
        message_template = MessageTemplateFactory(account=account)

        client.force_login(account)
        data = {
            "title": "",
            "body": "Invalid Body ${missing_curly",
        }
        response = client.post(target(message_template), data)
        form = response.context["form"]

        assert response.status_code == 200
        assert form.errors  # Form errors are present

    def test_message_template_update_other_account(self, target, client):
        account = AccountFactory()
        other_account = AccountFactory()
        message_template = MessageTemplateFactory(account=other_account)

        client.force_login(account)
        response = client.post(target(message_template))

        assert response.status_code == 404


@pytest.mark.django_db
class TestMessageTemplateDelete:
    @pytest.fixture
    def target(self):
        def _method(message_template: MessageTemplate):
            return reverse("message_template:delete", args=[message_template.id])

        return _method

    def test_message_template_delete_success(self, target, client):
        account = AccountFactory()
        message_template = MessageTemplateFactory(account=account)

        client.force_login(account)
        response = client.post(target(message_template))

        assert response.status_code == 302
        assert not MessageTemplate.objects.filter(id=message_template.id).exists()

    def test_message_template_delete_other_account(self, target, client):
        account = AccountFactory()
        other_account = AccountFactory()
        message_template = MessageTemplateFactory(account=other_account)

        client.force_login(account)
        response = client.post(target(message_template))

        assert response.status_code == 404
        assert MessageTemplate.objects.filter(id=message_template.id).exists()
