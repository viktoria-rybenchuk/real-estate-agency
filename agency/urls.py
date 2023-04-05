from django.urls import path

from agency.views import (
    index,
    AgentListView,
    AgentDetailView,
    PropertyListView,
    PropertyDetail,
    AgentCreateView,
    ClientCreateView, ClientUpdateView, PropertyCreateView, PropertyUpdateView, is_looking_for_house, AreaCreateView,
    AgentUpdateView, PropertyDeleteView
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
        "agents/<int:pk>update/",
        AgentUpdateView.as_view(),
        name="agent-update"
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
        PropertyCreateView.as_view(),
        name="property-create"
    ),
    path(
        "properties/<int:pk>/update/",
        PropertyUpdateView.as_view(),
        name="property-update"
    ),
    path(
        "properties/<int:pk>/delete/",
        PropertyDeleteView.as_view(),
        name="property-delete"
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
    ),
    path(
        "clients/<int:pk>/settled",
        is_looking_for_house,
        name="client-settled"
    ),
    path(
        "areas/create/",
        AreaCreateView.as_view(),
        name="area-create"
    ),

]

app_name = "agency"
