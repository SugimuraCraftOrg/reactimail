from string import Template
from re import compile

from django.forms import ModelForm, ValidationError
from .models import MessageTemplate

pattern = compile(r"\$\{(\w+)\}")


class MessageTemplateForm(ModelForm):
    class Meta:
        model = MessageTemplate
        fields = ["type", "title", "body", "tags"]

    def __init__(self, *args, **kwargs):
        # Capture the account from the view's context
        self.account = kwargs.pop("account", None)
        super().__init__(*args, **kwargs)

    def clean_body(self):
        body = self.cleaned_data.get("body")

        # Syntax checking and parameter extraction.
        try:
            tmpl = Template(body)
            parameters = pattern.findall(tmpl.template)
            # For checking the parameter list
            self.cleaned_data["parameters"] = parameters
        except ValueError as e:
            raise ValidationError(f"Template syntax error: {e}")

        return body
