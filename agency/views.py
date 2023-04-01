from django.db.models import QuerySet, Count
from django.db.models.functions import TruncMonth, ExtractMonth
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from agency.forms import PropertySearchForm, AgentCreationForm, ClientCreationForm, ClientUpdateForm
from agency.models import Agent, Property, Client, Area, Deal
#
def count_deal():
    Deal.objects.create(deal="j", agent_id=1)
    deals = Deal.objects.filter(date__month=4)
    return deals
print(count_deal())
def index(request: HttpRequest) -> HttpResponse:


    count_area = Area.objects.count()
    count_agent = Agent.objects.count()
    clients_found_home = Client.objects.filter(
        is_searching_for_property=False).count()
    context = {
        ""
        "count_agent": count_agent,
        "clients_found_home": clients_found_home,
        "count_area": count_area,
    }
    return render(request, "agency/index.html", context)


class AgentListView(ListView):
    model = Agent


class AgentDetailView(DetailView):
    model = Agent

    def get_context_data(self, **kwargs):
        agent = Agent.objects.get(id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        deal = self.request.GET.get("num_deals", 0)
        counter = agent.areas.filter(clients__is_searching_for_property=False).count()
        deal += counter
        context["num_deals"] = deal

        return context


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
    model = Property




class AgentCreateView(CreateView):
    model = Agent
    form_class = AgentCreationForm
    success_url = reverse_lazy("agency:agent-list")


class AreaListView(ListView):
    model = Area


# def succesfful_deal(pk):
#     agent = Agent.objects.get(id=pk)
#     counter = agent.areas.filter(clients__is_searching_for_property=False).count()
#     for area in agent.areas.all():
#         clients = area.clients.filter(is_searching_for_property=False)
#         area.clients.remove(*clients)
#     return counter
#
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientCreationForm
    success_url = reverse_lazy("agency:index")
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name = "agency/agent_form.html"

    def get_success_url(self):
        agent = self.request.user
        return reverse("agency:agent-detail", kwargs={"pk": agent.pk})