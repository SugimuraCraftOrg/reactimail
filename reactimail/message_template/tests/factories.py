import factory

from message_template.models import MessageTemplate


class MessageTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MessageTemplate

    account = factory.SubFactory("account.tests.factories.AccountFactory")
    type = MessageTemplate.TYPES.TEXT
    title = factory.Sequence(lambda n: f"title{n}")
    body = factory.Sequence(lambda n: f"body{n}")
