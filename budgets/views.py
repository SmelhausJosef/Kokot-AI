from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from accounts.mixins import OrganizationScopedMixin, RoleRequiredMixin
from accounts.models import OrganizationRole

from .forms import BudgetForm
from .models import Budget


class BudgetListView(OrganizationScopedMixin, ListView):
    model = Budget
    context_object_name = "budgets"
    template_name = "budgets/budget_list.html"

    def get_queryset(self):
        return (
            Budget.objects.filter(order__construction__organization=self.organization)
            .select_related("order", "order__construction")
        )


class BudgetDetailView(OrganizationScopedMixin, DetailView):
    model = Budget
    context_object_name = "budget"
    template_name = "budgets/budget_detail.html"

    def get_queryset(self):
        return (
            Budget.objects.filter(order__construction__organization=self.organization)
            .select_related("order", "order__construction")
            .prefetch_related("headers")
        )


class BudgetCreateView(RoleRequiredMixin, CreateView):
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budgets:budget-list")
    required_roles = {OrganizationRole.CEO, OrganizationRole.BUDGET_MANAGER}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = self.organization
        return kwargs

    def get_success_url(self):
        return reverse("budgets:budget-list")
