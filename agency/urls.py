from django.urls import path

from agency.views import index, AgentListView

urlpatterns = [
    path("", index, name="index"),
    path("agents/", AgentListView.as_view(), name="agent-list")
]

app_name = "agency"
