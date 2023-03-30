from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from agency.models import Agent, Client


class AgentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Agent
        fields = ("username", "first_name", "last_name", "email")


class PropertySearchForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        required=False,
        label="",
        widget=forms.TextInput(attrs=
                               {"placeholder": "Search by title"})
    )


class ClientCreationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone number'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].initial = '+44'

    class Meta:
        model = Client
        fields = "__all__"

    def clean_phone_number(self) -> str:
        return validate_phone_number(self.cleaned_data["phone_number"])


def validate_phone_number(phone_number: str) -> str:
    phone_number = phone_number.replace(" ", "")
    if phone_number[:3] != "+44":
        raise ValidationError("Phone number should consist code of country")
    if len(phone_number) != 5:
        raise ValidationError("Phone number should consist 11 numbers")
    elif not phone_number[1:].isdigit():
        raise ValidationError("Phone number should consist digit")
    return phone_number
