from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Count
from django.db.models.functions import TruncMonth
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import url
from django.urls import reverse_lazy, reverse
from django.utils.datetime_safe import datetime
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView, DeleteView
)

from agency.forms import (
    PropertySearchForm,
    AgentCreationForm,
    ClientCreationForm,
    ClientUpdateForm,
    AgentSearchForm, PropertyCreationForm, AreaCreationForm
)
from agency.models import (
    Agent,
    Property,
    Client,
    Area,
    Deal
)

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
    if not max_result:
        return {
            "agent": "-",
            "max_deals": 0
        }
    agent_id = max_result["agent"]
    agent = Agent.objects.get(id=agent_id)
    full_name_worker = f"{agent.first_name} {agent.last_name}"
    return {
        "agent": full_name_worker,
        "max_deals": max_result["count_deal"]
    }


@login_required
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


class AgentListView(LoginRequiredMixin, ListView):
    model = Agent
    queryset = Agent.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(AgentListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")
        context["search_form"] = AgentSearchForm(initial={"last_name": last_name})
        return context

    def get_queryset(self) -> QuerySet:
        form = AgentSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                last_name__icontains=form.cleaned_data["last_name"]
            )
        return self.queryset


class AgentDetailView(LoginRequiredMixin, DetailView):
    model = Agent

    def get_context_data(self, **kwargs) -> dict:
        agent = Agent.objects.get(id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        deal = self.request.GET.get("num_deals", 0)
        counter = agent.areas.filter(clients__is_searching_for_property=False).count()
        deal += counter
        context["num_deals"] = deal

        return context


class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(PropertyListView, self).get_context_data(**kwargs)
        address = self.request.GET.get("address", "")
        context["search_form"] = PropertySearchForm(initial={"address": address})
        return context

    def get_queryset(self) -> QuerySet:
        form = PropertySearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                address__icontains=form.cleaned_data["address"]
            )
        return self.queryset


class PropertyDetail(LoginRequiredMixin, DetailView):
    model = Property
    queryset = Property.objects.prefetch_related("area")


class AgentCreateView(LoginRequiredMixin, CreateView):
    model = Agent
    form_class = AgentCreationForm
    success_url = reverse_lazy("agency:agent-list")


class AgentUpdateView(LoginRequiredMixin, UpdateView):
    model = Agent
    form_class = AgentCreationForm
    success_url = reverse_lazy("agency:agent-list")


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientCreationForm
    success_url = reverse_lazy("agency:index")


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyCreationForm
    success_url = reverse_lazy("agency:property-list")


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyCreationForm
    template_name = "agency/property_form.html"

    def get_success_url(self) -> url:
        agent = self.request.user
        return reverse(
            "agency:agent-detail", kwargs={"pk": agent.pk}
        )


class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = "agency/property_delete_confirmation.html"
    success_url = reverse_lazy("agency:property-list")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name = "agency/client_form.html"

    def get_success_url(self) -> url:
        agent = self.request.user
        return reverse(
            "agency:agent-detail", kwargs={"pk": agent.pk}
        )


class AreaCreateView(LoginRequiredMixin, CreateView):
    model = Area
    form_class = AreaCreationForm
    success_url = reverse_lazy("agency:index")


def is_looking_for_house(
        request: HttpRequest,
        pk: int
) -> HttpResponseRedirect:
    client = get_object_or_404(Client, pk=pk)
    if client.is_searching_for_property is True:
        client.is_searching_for_property = False
        client.save()
    return HttpResponseRedirect(
        reverse_lazy(
            "agency:agent-detail", args=[request.user.id]
        )
    )
