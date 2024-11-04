from django.db import models

from reactimail.models import BaseModelMixin


class Tag(BaseModelMixin):
    account = models.ForeignKey("account.ReactiMailUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
