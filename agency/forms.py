from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from agency.models import Agent, Client, Property, Area

PHONE_CODE_COUNTRY = "+44"
LENGH_PHONE_NUMBER = 11


class AgentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Agent
        fields = ("username", "first_name", "last_name", "email")


class AreaCreationForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = "__all__"


class PropertyCreationForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["additional_info"]


class PropertySearchForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        required=False,
        label="",
        widget=forms.TextInput(attrs=
                               {"placeholder": "Search by title"})
    )


class AgentSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=60,
        required=False,
        label="",
        widget=forms.TextInput(attrs=
                               {"placeholder": "Search by last name"})
    )


class ClientCreationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone number'}
        )
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].initial = PHONE_CODE_COUNTRY

    class Meta:
        model = Client
        fields = "__all__"

    def clean_phone_number(self) -> str:
        return validate_phone_number(self.cleaned_data["phone_number"])


def validate_phone_number(phone_number: str) -> str:
    phone_number = phone_number.replace(" ", "")
    if phone_number[:3] != PHONE_CODE_COUNTRY:
        raise ValidationError(
            f"Phone number should consist phone "
            f"code of country {PHONE_CODE_COUNTRY}"
        )
    if len(phone_number)[1:] != LENGH_PHONE_NUMBER:
        raise ValidationError(f"Phone number should consist {LENGH_PHONE_NUMBER} numbers."
                              f"You have {phone_number} numbers")
    elif not phone_number[1:].isdigit():
        raise ValidationError("Phone number should consist digit")
    return phone_number
