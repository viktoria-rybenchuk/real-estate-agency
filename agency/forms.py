from django import forms


class PropertySearchForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        required=False,
        label="",
        widget=forms.TextInput(attrs=
            {"placeholder": "Search by title"})
    )