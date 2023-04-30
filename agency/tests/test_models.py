from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.models import Area, Deal, Property, Client


class AreaModelTest(TestCase):
    def setUp(self) -> None:
        self.agent = get_user_model().objects.create(
            username="testagent",
            first_name="Test",
            last_name="Agent",
            email="agent@gmail.com"
        )
        self.area = Area.objects.create(
            name="Brixton",
            agent=self.agent
        )

    def test_str_area_model(self) -> None:
        area = self.area
        self.assertEqual(str(area), area.name)

    def test_str_agent_model(self) -> None:
        agent = self.agent
        self.assertEqual(
            str(agent),
            f"{agent.username} "
            f"({agent.first_name}"
            f" {agent.last_name})"
        )

    def test_str_deal_model(self) -> None:
        agent = self.agent
        deal = Deal.objects.create(
            deal="TownHouse",
            agent=agent,
            date="2023-12-01"
        )
        self.assertEqual(
            str(deal),
            f"{deal.deal} {deal.agent} {deal.date}"
        )

    def test_str_property_model(self) -> None:
        property = Property.objects.create(
            address="Town Street 2",
            price=500000,
            description="New house with 3 rooms",
            property_type="apartment",
            is_available=True,
            created_at="2023-12-3",
            area=self.area,
            agent=self.agent
        )
        self.assertEqual(str(property), property.address)

    def test_str_client_model(self) -> None:
        client = Client.objects.create(
            first_name="Jack",
            last_name="Hogard",
            email="jackHogward@gmail.com",
            phone_number="+45 345 566 78 88",
            is_searching_for_property=True,
            additional_info="No additional info",
            search_area=self.area
        )
        self.assertEqual(
            str(client),
            f"{client.first_name} "
            f"{client.last_name}"
        )
