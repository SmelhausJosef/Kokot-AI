from io import BytesIO

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from openpyxl import Workbook

from accounts.models import Organization, OrganizationMembership, OrganizationRole
from budgets.models import Budget
from construction.models import Construction, Order

User = get_user_model()


def build_order(organization):
    construction = Construction.objects.create(name="Site A", organization=organization)
    return Order.objects.create(name="Order A", construction=construction)


def build_invalid_excel_payload():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Zakázka"
    sheet.append(["Wrong", "Headers"])
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


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


@pytest.mark.django_db
def test_budget_create_rolls_back_on_import_error(settings, tmp_path, client):
    settings.MEDIA_ROOT = tmp_path
    organization = Organization.objects.create(name="Alpha Build")
    user = User.objects.create_user(username="bm@example.com", password="StrongPass123!")
    OrganizationMembership.objects.create(
        user=user,
        organization=organization,
        role=OrganizationRole.BUDGET_MANAGER,
    )
    order = build_order(organization)

    client.login(username="bm@example.com", password="StrongPass123!")
    payload = {
        "order": order.id,
        "name": "Budget A",
        "excel_file": SimpleUploadedFile("budget.xlsx", build_invalid_excel_payload()),
    }
    response = client.post(reverse("budgets:budget-create"), payload)
    assert response.status_code == 200
    assert "excel_file" in response.context["form"].errors
    assert not Budget.objects.filter(order=order).exists()
    assert not list(tmp_path.rglob("*.xlsx"))


@pytest.mark.django_db
def test_budget_list_scoped_to_organization(client):
    organization_a = Organization.objects.create(name="Alpha Build")
    organization_b = Organization.objects.create(name="Beta Build")
    user = User.objects.create_user(username="bm@example.com", password="StrongPass123!")
    OrganizationMembership.objects.create(
        user=user,
        organization=organization_a,
        role=OrganizationRole.BUDGET_MANAGER,
    )
    order_a = build_order(organization_a)
    order_b = build_order(organization_b)
    budget_a = Budget.objects.create(order=order_a, name="Budget A")
    Budget.objects.create(order=order_b, name="Budget B")

    client.login(username="bm@example.com", password="StrongPass123!")
    response = client.get(reverse("budgets:budget-list"))
    assert response.status_code == 200
    budgets = list(response.context["budgets"])
    assert budget_a in budgets
    assert all(budget.order.construction.organization_id == organization_a.id for budget in budgets)


@pytest.mark.django_db
def test_budget_detail_scoped_to_organization(client):
    organization_a = Organization.objects.create(name="Alpha Build")
    organization_b = Organization.objects.create(name="Beta Build")
    user = User.objects.create_user(username="bm@example.com", password="StrongPass123!")
    OrganizationMembership.objects.create(
        user=user,
        organization=organization_a,
        role=OrganizationRole.BUDGET_MANAGER,
    )
    order_b = build_order(organization_b)
    budget_b = Budget.objects.create(order=order_b, name="Budget B")

    client.login(username="bm@example.com", password="StrongPass123!")
    response = client.get(reverse("budgets:budget-detail", args=[budget_b.pk]))
    assert response.status_code == 404
