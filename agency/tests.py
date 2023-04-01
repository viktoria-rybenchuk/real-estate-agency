from django.test import TestCase

from agency.models import Agent


class ModelsTest(TestCase):
    def test_agent_str(self):
        agent = Agent.objects.create(username="testuser", first_name="Test", last_name="User")
        self.assertEqual(str(agent), f"{agent.username} ({agent.first_name} {agent.last_name})")