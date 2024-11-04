# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        # Capture the account from the view's context
        self.account = kwargs.pop("account", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            Tag.objects.filter(account=self.account, name=name)
            .exclude(pk=self.instance.id)
            .exists()
        ):
            raise ValidationError(
                "A tag with this name already exists for your account."
            )
        return name
