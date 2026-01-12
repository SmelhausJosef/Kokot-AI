from django.urls import path

from . import views

app_name = "budgets"

urlpatterns = [
    path("budgets/", views.BudgetListView.as_view(), name="budget-list"),
    path("budgets/new/", views.BudgetCreateView.as_view(), name="budget-create"),
    path("budgets/<int:pk>/", views.BudgetDetailView.as_view(), name="budget-detail"),
]
