from django.urls import path

from agency.views import index, AgentListView, AgentDetailView, PropertyListView, PropertyDetail

urlpatterns = [
    path("", index, name="index"),
    path("agents/", AgentListView.as_view(), name="agent-list"),
    path("agents/<int:pk>/detail/", AgentDetailView.as_view(), name="agent-detail"),
    path("properties/", PropertyListView.as_view(), name="property-list"),
    path("properties/<int:pk>/detail/", PropertyDetail.as_view(), name="property-detail")
]

app_name = "agency"
