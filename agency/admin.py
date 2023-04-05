from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from agency.models import Agent, Area, Property, Client, Deal


@admin.register(Agent)
class AgentAdmin(UserAdmin):
    search_fields = ("last_name",)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    filter = ("price", "area",)
    search_fields = ("area",)
    list_display = ("address", "price", "area",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("last_name",)
    filter = ("is_searching_for_property",)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    filter = ("-date",)
