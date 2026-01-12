from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from accounts.services import get_active_membership

from .forms import ConstructionForm, ContractForWorkForm, OrderForm
from .models import Construction, ContractForWork, Order


class OrganizationScopedMixin(LoginRequiredMixin):
    membership = None
    organization = None

    def dispatch(self, request, *args, **kwargs):
        self.membership = get_active_membership(request.user)
        self.organization = self.membership.organization
        return super().dispatch(request, *args, **kwargs)


class ConstructionListView(OrganizationScopedMixin, ListView):
    model = Construction
    context_object_name = "constructions"
    template_name = "construction/construction_list.html"

    def get_queryset(self):
        return Construction.objects.filter(organization=self.organization)


class ConstructionDetailView(OrganizationScopedMixin, DetailView):
    model = Construction
    context_object_name = "construction"
    template_name = "construction/construction_detail.html"

    def get_queryset(self):
        return Construction.objects.filter(organization=self.organization)


class ConstructionCreateView(OrganizationScopedMixin, CreateView):
    form_class = ConstructionForm
    template_name = "construction/construction_form.html"
    success_url = reverse_lazy("construction:construction-list")

    def form_valid(self, form):
        form.instance.organization = self.organization
        return super().form_valid(form)


class OrderListView(OrganizationScopedMixin, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "construction/order_list.html"

    def get_queryset(self):
        return Order.objects.filter(construction__organization=self.organization).select_related("construction")


class OrderDetailView(OrganizationScopedMixin, DetailView):
    model = Order
    context_object_name = "order"
    template_name = "construction/order_detail.html"

    def get_queryset(self):
        return Order.objects.filter(construction__organization=self.organization).select_related("construction")


class OrderCreateView(OrganizationScopedMixin, CreateView):
    form_class = OrderForm
    template_name = "construction/order_form.html"
    success_url = reverse_lazy("construction:order-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = self.organization
        return kwargs

    def form_valid(self, form):
        if form.instance.construction.organization_id != self.organization.id:
            raise PermissionDenied
        return super().form_valid(form)


class ContractForWorkCreateView(OrganizationScopedMixin, CreateView):
    form_class = ContractForWorkForm
    template_name = "construction/contract_form.html"

    def _get_order(self) -> Order:
        if hasattr(self, "_order"):
            return self._order
        self._order = get_object_or_404(
            Order, pk=self.kwargs["order_id"], construction__organization=self.organization
        )
        if hasattr(self._order, "contract"):
            raise PermissionDenied
        return self._order

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self._get_order()
        return kwargs

    def form_valid(self, form):
        form.instance.order = self._get_order()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("construction:order-detail", kwargs={"pk": self._get_order().pk})
