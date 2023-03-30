from django.urls import path

from agency.views import (
    index,
    AgentListView,
    AgentDetailView,
    PropertyListView,
    PropertyDetail,
    AgentCreateView,
    AreaListView,
    CreateClientView
)

urlpatterns = [
    path("", index, name="index"),
    path("agents/", AgentListView.as_view(), name="agent-list"),
    path("agents/<int:pk>/detail/", AgentDetailView.as_view(), name="agent-detail"),
    path("agents/create/", AgentCreateView.as_view(), name="agent-create"),
    path("properties/", PropertyListView.as_view(), name="property-list"),
    path("properties/<int:pk>/detail/", PropertyDetail.as_view(), name="property-detail"),
    path("areas/", AreaListView.as_view(), name="area-list"),
    path("clients/", CreateClientView.as_view(), name="client-create")

]

app_name = "agency"
