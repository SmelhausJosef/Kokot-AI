from django.contrib import admin

from .models import Construction, ContractForWork, Order, Residual


@admin.register(Construction)
class ConstructionAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "location")
    search_fields = ("name", "organization__name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "construction")
    search_fields = ("name", "construction__name")
    filter_horizontal = ("managers",)


@admin.register(ContractForWork)
class ContractForWorkAdmin(admin.ModelAdmin):
    list_display = ("contract_number", "order", "contractor_share")
    search_fields = ("contract_number", "order__name")


@admin.register(Residual)
class ResidualAdmin(admin.ModelAdmin):
    list_display = ("contract_for_work", "percentage", "end_date")
