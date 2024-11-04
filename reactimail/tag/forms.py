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

    def clean_name(self) -> str:
        """
        Validate that the tag name is unique for the account.

        Returns:
            str: The validated tag name
        Raises:
            ValidationError: If a tag with the same name exists for the account
        """
        name = self.cleaned_data.get("name")
        existing_tags = Tag.objects.filter(account=self.account, name=name)
        if self.instance.id:
            existing_tags = existing_tags.exclude(id=self.instance.id)
        if existing_tags.exists():
            raise ValidationError(
                "A tag with this name already exists for your account."
            )
        return name
