from django.db import models

from reactimail.models import BaseModelMixin


class Tag(BaseModelMixin):
    account = models.ForeignKey(
        "account.ReactiMailUser",
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name="Account",
        help_text="The account that owns this tag",
    )
    name = models.CharField(
        max_length=200, verbose_name="Tag Name", help_text="The name of the tag"
    )

    class Meta:
        unique_together = ["account", "name"]
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name
