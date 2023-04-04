from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.models import Area


class ModelTest(TestCase):
    def test_str_area(self):
        agent = get_user_model().objects.create_user(
            username="test_user",
            first_name = "test",
            last_name = "user"
        )
        area = Area.objects.create(name="Brinx", agent=agent)

        self.assertEqual(str(area), area.name)
