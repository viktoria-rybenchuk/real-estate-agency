from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.forms import ClientCreationForm
from agency.models import Area


class FormTest(TestCase):
    def setUp(self) -> None:
        self.agent = get_user_model().objects.create(
            first_name="Test",
            last_name="Jo",
            email="jo@gmail.com"
        )
        self.area = Area.objects.create(name="Brixton", agent=self.agent)

    def test_clean_phone_number(self) -> None:
        form_data = {
            "first_name": "Jo",
            "last_name": "Swagger",
            "email": "swagger@gmail.com",
            "phone_number": "+44 123 456 78901",
            "search_area": "1"
        }
        form = ClientCreationForm(form_data)

        self.assertTrue(form.is_valid())

    def test_phone_number_should_be_not_more_than_11(self) -> None:
        form_data = {
            "first_name": "Jo",
            "last_name": "Swagger",
            "email": "swagger@gmail.com",
            "phone_number": "+44 123 456 789012222222",
            "search_area": "1"
        }
        form = ClientCreationForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_phone_number_should_be_not_less_than_11(self) -> None:
        form_data = {
            "first_name": "Jo",
            "last_name": "Swagger",
            "email": "swagger@gmail.com",
            "phone_number": "+44 123 ",
            "search_area": "1"
        }
        form = ClientCreationForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_phone_number_first_3_characters_should_be_code_of_country(self) -> None:
        form_data = {
            "first_name": "Jo",
            "last_name": "Swagger",
            "email": "swagger@gmail.com",
            "phone_number": "000 123 123 456 23",
            "search_area": "1"
        }
        form = ClientCreationForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
