from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from agency.forms import PropertySearchForm
from agency.models import Agent, Property, Client, Area


def index(request: HttpRequest) -> HttpResponse:
    count_area = Area.objects.count()
    count_agent = Agent.objects.count()
    clients_found_home = Client.objects.filter(
        is_searching_for_property=False).count()
    context = {
        "count_agent": count_agent,
        "clients_found_home": clients_found_home,
        "count_area": count_area
    }
    return render(request, "agency/index.html", context)


class AgentListView(ListView):
    model = Agent


class AgentDetailView(DetailView):
    model = Agent


class PropertyListView(ListView):
    model = Property
    queryset = Property.objects.select_related("area")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(PropertyListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = PropertySearchForm(initial={"title": title})
        return context

    def get_queryset(self) -> QuerySet:
        form = PropertySearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return self.queryset


class PropertyDetail(DetailView):
    model = property
