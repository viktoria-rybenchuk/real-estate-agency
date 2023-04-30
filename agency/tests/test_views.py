from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse, reverse_lazy

from agency.models import Client, Area, Deal, Property

AGENT_URL = reverse("agency:agent-list")
PROPERTY_URL = reverse("agency:property-list")
INDEX_URL = reverse("agency:index")
PAGINATION = 5


class PublicCarTest(TestCase):
    def test_login_required_agent(self) -> None:
        response = self.client.get(AGENT_URL)
        self.assertNotEqual(response, 200)

    def test_login_required_property(self) -> None:
        response = self.client.get(PROPERTY_URL)
        self.assertNotEqual(response, 200)

    def test_login_required_index(self) -> None:
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response, 200)


class PrivateAgentTest(TestCase):
    def setUp(self) -> None:
        self.agent = get_user_model().objects.create_user(
            username="Agent", password="12345"
        )
        self.agent1 = get_user_model().objects.create_user(
            username="first",
            first_name="new",
            last_name="test",
            password="123455",
            email="new@gmail.com"
        )
        self.agent2 = get_user_model().objects.create_user(
            username="second",
            first_name="second",
            last_name="test",
            password="123455",
            email="second@gmail.com"
        )
        self.agent3 = get_user_model().objects.create_user(
            username="third",
            first_name="third",
            last_name="test",
            password="123455",
            email="third@gmail.com"
        )
        self.agent4 = get_user_model().objects.create_user(
            username="fourth",
            first_name="fourth",
            last_name="test",
            password="123455",
            email="fourth@gmail.com"
        )
        self.area = Area.objects.create(name="Brixton", agent=self.agent)
        self.property = Property.objects.create(
            address="123 Test Street",
            price=100000,
            description="Test property",
            property_type="House",
            is_available=True,
            area=self.area,
            agent=self.agent
        )

        self.client.force_login(self.agent)

    def test_template_for_agent_list(self) -> None:
        response = self.client.get(AGENT_URL)
        self.assertTemplateUsed(
            response, "agency/agent_list.html"
        )

    def test_agent_detail_page(self) -> None:
        response = self.client.get(reverse(
            "agency:agent-detail", args=[self.agent.id])
        )
        num_deals = Deal.objects.filter(agent=self.agent).count()
        self.assertEqual(response.context["num_deals"], num_deals)

        self.assertEqual(response.status_code, 200)

    def test_search_agent_by_last_name(self) -> None:
        get_user_model().objects.create_user(
            username="testUser",
            first_name="Test",
            last_name="User",
        )
        key = "Us"
        response = self.client.get(
            AGENT_URL + f"?last_name={key}"
        )
        agent_list = get_user_model().objects.filter(
            last_name__icontains=key
        )
        self.assertEqual(
            list(response.context["agent_list"]), list(agent_list)
        )

    def test_agent_list_paginated_correctly(self) -> None:
        response = self.client.get(AGENT_URL)
        self.assertEqual(len(response.context["agent_list"]), PAGINATION)

    def test_settled_client(self) -> None:
        area = self.area
        client = Client.objects.create(
            first_name="Jo",
            last_name="Wolf",
            email="jo@gmail.com",
            phone_number="+45 1111111111",
            is_searching_for_property=True,
            search_area=area
        )
        response = self.client.post(reverse_lazy(
            "agency:client-settled", args=[self.agent.pk])
        )
        self.assertRedirects(
            response, reverse_lazy("agency:agent-detail", args=[self.agent.pk])
        )
        client.refresh_from_db()
        self.assertFalse(client.is_searching_for_property)

    def test_agent_list_ordered_by_last_name(self) -> None:
        response = self.client.get(AGENT_URL)
        agent_list = get_user_model().objects.all().order_by("last_name")
        agent_context = response.context["agent_list"]

        self.assertEqual(
            list(agent_context),
            list(agent_list[: len(agent_context)]),
        )


class PrivateProperty(TestCase):
    def setUp(self) -> None:
        self.agent = get_user_model().objects.create_user(
            username="Agent", password="12345"
        )
        self.area = Area.objects.create(name="Brixton", agent=self.agent)
        self.client.force_login(self.agent)
        self.property = Property.objects.create(
            address="123 Test Street",
            price=100000,
            description="Test property",
            property_type="House",
            is_available=True,
            area=self.area,
            agent=self.agent
        )

    def test_search_property_by_address(self) -> None:
        key = "test"
        response = self.client.get(
            PROPERTY_URL + f"?address={key}"
        )
        property_list = Property.objects.filter(
            address__icontains=key
        )
        self.assertEqual(
            list(response.context["property_list"]), list(property_list)
        )

    def test_property_detail_page(self) -> None:
        response = self.client.get(reverse(
            "agency:property-detail", args=[self.property.id])
        )
        self.assertEqual(response.status_code, 200)
