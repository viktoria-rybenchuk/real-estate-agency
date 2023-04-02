from django.db.models import QuerySet, Count
from django.db.models.functions import TruncMonth
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from agency.forms import PropertySearchForm, AgentCreationForm, ClientCreationForm, ClientUpdateForm
from agency.models import Agent, Property, Client, Area, Deal

MONTHS = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

CURRENT_YEAR = datetime.now().year


def get_deals_per_month() -> dict:
    deals = Deal.objects.filter(date__year=CURRENT_YEAR).annotate(
        month=TruncMonth("date")
    ).values("month").annotate(
        sum=Count("deal")).order_by("month")
    deal_list = [sum_deal["sum"] for sum_deal in deals]
    month_list = [
        MONTHS.get(date.month) for date in deals.values_list("month", flat=True)
    ]
    data = {
        "month": month_list,
        "count_deals": deal_list
    }
    return data


def get_best_worker_of_month() -> dict:
    previous_month = datetime.now().month - 1
    max_result = Deal.objects.filter(
        date__month=previous_month).values(
        "agent").annotate(
        count_deal=Count("deal")).order_by(
        "-count_deal").first()
    agent_id = max_result["agent"]
    agent = Agent.objects.get(id=agent_id)
    full_name_worker = f"{agent.first_name} {agent.last_name}"
    return {
        "agent": full_name_worker,
        "max_deals": max_result["count_deal"]
    }


def index(request: HttpRequest) -> HttpResponse:
    monthly_deals = get_deals_per_month().get("count_deals")
    month = get_deals_per_month()["month"]
    best_worker = get_best_worker_of_month().get("agent")
    max_deals = get_best_worker_of_month().get("max_deals")
    count_area = Area.objects.count()
    clients_found_home = Client.objects.filter(
        is_searching_for_property=False).count()
    active_client = Client.objects.filter(
        is_searching_for_property=True).count()
    context = {
        "best_worker": best_worker,
        "max_deals": max_deals,
        "month": month,
        "monthly_deals": monthly_deals,
        "current_year": CURRENT_YEAR,
        "clients_found_home": clients_found_home,
        "active_client": active_client,
        "count_area": count_area,
    }
    return render(request, "agency/index.html", context)


class AgentListView(ListView):
    model = Agent
    paginate_by = 10


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
    paginate_by = 10

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
