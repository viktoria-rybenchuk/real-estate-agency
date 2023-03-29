from django import forms
from django.contrib.auth.forms import UserCreationForm

from agency.models import Agent


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
