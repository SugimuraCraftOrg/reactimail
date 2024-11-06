import re
from string import Template

from django.db import models

from tag.models import Tag
from reactimail.models import BaseModelMixin

body_parameter_pattern = re.compile(r"\$\{(\w+)\}")


class MessageTemplateTypes(models.TextChoices):
    """The type of Email body."""

    TEXT = "text"
    HTML = "html"


class MessageTemplate(BaseModelMixin):

    TYPES = MessageTemplateTypes

    account = models.ForeignKey(
        "account.ReactiMailUser",
        on_delete=models.CASCADE,
        related_name="message_templates",
        verbose_name="Account",
        help_text="The account that owns this message template",
    )
    type = models.CharField(
        max_length=10,
        choices=TYPES.choices,
        verbose_name="Email Type",
        help_text="The type of the message (HTML or Text)",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Message Title",
        help_text="The title of the message template",
    )
    body = models.TextField(
        verbose_name="Message Body", help_text="The body of the message template"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="message_templates",
        verbose_name="Tags",
        help_text="Tags associated with this message template",
    )

    @property
    def body_parameters(self) -> list[str]:
        tmpl = Template(self.body)
        return sorted(body_parameter_pattern.findall(tmpl.template))

    @property
    def tag_names(self) -> str:
        return ",".join(tag.name for tag in self.tags.order_by("name").all())

    def __str__(self):
        v = self.title
        if self.tag_names != "":
            v = v + f" (tags={self.tag_names})"
        return v
