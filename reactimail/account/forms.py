# forms.py
from django import forms
from django.contrib.auth import authenticate


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254, required=True)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, required=True
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
