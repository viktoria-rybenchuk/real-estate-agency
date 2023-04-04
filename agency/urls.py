from django.urls import path

from agency.views import (
    index,
    AgentListView,
    AgentDetailView,
    PropertyListView,
    PropertyDetail,
    AgentCreateView,
    ClientCreateView, ClientUpdateView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "agents/",
        AgentListView.as_view(),
        name="agent-list"
    ),
    path(
        "agents/<int:pk>/detail/",
        AgentDetailView.as_view(),
        name="agent-detail"),
    path(
        "agents/create/",
        AgentCreateView.as_view(),
        name="agent-create"
    ),
    path(
        "properties/",
        PropertyListView.as_view(),
        name="property-list"
    ),
    path(
        "properties/<int:pk>/detail/",
        PropertyDetail.as_view(),
        name="property-detail"
    ),
    path(
        "properties/create/",
        ClientCreateView.as_view(),
        name="property-create"
    ),

    path(
        "clients/create/",
        ClientCreateView.as_view(),
        name="client-create"
    ),
    path(
        "clients/<int:pk>/update/",
        ClientUpdateView.as_view(),
        name="client-update"
    )

]

app_name = "agency"
