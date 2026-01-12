from django.contrib import admin

from .models import Budget, BudgetHeader, BudgetItem, BudgetItemAmount, BudgetPeriod


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "created_at")
    search_fields = ("name", "order__name")


@admin.register(BudgetHeader)
class BudgetHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "budget", "parent")
    search_fields = ("title", "budget__name")


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "header", "price_for_unit")
    search_fields = ("code", "description")


@admin.register(BudgetPeriod)
class BudgetPeriodAdmin(admin.ModelAdmin):
    list_display = ("budget", "status", "created_at")
    list_filter = ("status",)


@admin.register(BudgetItemAmount)
class BudgetItemAmountAdmin(admin.ModelAdmin):
    list_display = ("budget_item", "period", "amount")
