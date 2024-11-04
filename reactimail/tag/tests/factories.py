import factory

from tag.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    account = factory.SubFactory("account.tests.factories.AccountFactory")
    name = factory.Sequence(lambda n: f"tag{n}")
