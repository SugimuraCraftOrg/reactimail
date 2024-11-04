# forms.py
from django import forms
from django.contrib.auth import authenticate


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
        help_text="Enter the email address you registered with",
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True,
        help_text="Enter your password (minimum 8 characters)",
        error_messages={"min_length": "Password must be at least 8 characters long"},
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError("Email or password is incorrect.")

        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user
