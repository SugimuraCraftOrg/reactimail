import pytest

from account.tests.factories import AccountFactory
from tag.models import Tag
from message_template.models import MessageTemplate
from .factories import MessageTemplateFactory


@pytest.mark.django_db
class TestMessageTemplateModel:
    def test_body_parameters_extraction(self):
        """Test message template with specific parameters.
        Also tests that parameter names are sorted.
        """
        user = AccountFactory()
        body_text = "Hello ${first_name}, your order ${order_id} is confirmed!\r\nyour member id is ${member_id}."
        message_template = MessageTemplateFactory(account=user, body=body_text)

        parameters = message_template.body_parameters

        assert parameters == ["first_name", "member_id", "order_id"]

    def test_body_parameters_no_parameters(self):
        """Test message template without any placeholders."""
        user = AccountFactory()
        body_text = "Hello, welcome to our service!"
        message_template = MessageTemplateFactory(account=user, body=body_text)

        parameters = message_template.body_parameters

        assert parameters == []

    def test_tag_names(self):
        """Test message template with associated tags.
        Also tests that tag names are sorted.
        """
        user = AccountFactory()
        tag1 = Tag.objects.create(name="welcome", account=user)
        tag2 = Tag.objects.create(name="newsletter", account=user)
        message_template = MessageTemplateFactory(account=user)
        message_template.tags.set([tag1, tag2])

        tag_names = message_template.tag_names

        assert tag_names == "newsletter,welcome"

    def test_tag_names_no_tags(self):
        """Test message template without any tags."""
        user = AccountFactory()
        message_template = MessageTemplateFactory(account=user)

        tag_names = message_template.tag_names

        assert tag_names == ""
