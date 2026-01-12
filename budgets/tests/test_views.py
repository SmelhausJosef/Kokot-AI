import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Organization, OrganizationMembership, OrganizationRole
from budgets.models import Budget
from construction.models import Construction, Order

User = get_user_model()


def build_order(organization):
    construction = Construction.objects.create(name="Site A", organization=organization)
    return Order.objects.create(name="Order A", construction=construction)


@pytest.mark.django_db
def test_budget_create_requires_budget_role(client):
    organization = Organization.objects.create(name="Alpha Build")
    user = User.objects.create_user(username="cm@example.com", password="StrongPass123!")
    OrganizationMembership.objects.create(
        user=user,
        organization=organization,
        role=OrganizationRole.CONSTRUCTION_MANAGER,
    )
    build_order(organization)

    client.login(username="cm@example.com", password="StrongPass123!")
    response = client.get(reverse("budgets:budget-create"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_budget_create_allows_sub_budget_manager(client):
    organization = Organization.objects.create(name="Alpha Build")
    user = User.objects.create_user(username="subbm@example.com", password="StrongPass123!")
    OrganizationMembership.objects.create(
        user=user,
        organization=organization,
        role=OrganizationRole.SUB_BUDGET_MANAGER,
    )
    order = build_order(organization)

    client.login(username="subbm@example.com", password="StrongPass123!")
    payload = {"order": order.id, "name": "Budget A"}
    response = client.post(reverse("budgets:budget-create"), payload)
    assert response.status_code == 302
    assert Budget.objects.filter(order=order, name="Budget A").exists()
