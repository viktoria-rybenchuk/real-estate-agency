from django.urls import path

from agency.views import index, AgentListView, AgentDetailView

urlpatterns = [
    path("", index, name="index"),
    path("agents/", AgentListView.as_view(), name="agent-list"),
    path("agents/<int:pk>/", AgentDetailView.as_view(), name="agent-detail")
]

app_name = "agency"
