from random import randint
from uuid import uuid4

from faker import Faker
from django.db import models


def generate_random_nickname():
    faker = Faker()
    return f"{faker.word()}-{faker.word()}-{randint(100000, 999999)}"


class BaseModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
