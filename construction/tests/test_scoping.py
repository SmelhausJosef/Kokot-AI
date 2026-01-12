import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Organization, OrganizationMembership, OrganizationRole
from construction.models import Construction, ContractForWork, Order, Residual

User = get_user_model()


@pytest.mark.django_db
def test_construction_list_scoped_to_organization(client):
    org_a = Organization.objects.create(name="Org A")
    org_b = Organization.objects.create(name="Org B")
    user = User.objects.create_user(username="user@example.com", password="StrongPass123!")
    OrganizationMembership.objects.create(user=user, organization=org_a, role=OrganizationRole.CEO)

    Construction.objects.create(organization=org_a, name="Alpha Site")
    Construction.objects.create(organization=org_b, name="Beta Site")

    client.login(username="user@example.com", password="StrongPass123!")
    response = client.get(reverse("construction:construction-list"))

    constructions = response.context["constructions"]
    names = {construction.name for construction in constructions}
    assert names == {"Alpha Site"}


@pytest.mark.django_db
def test_order_list_scoped_to_organization(client):
    org_a = Organization.objects.create(name="Org A")
    org_b = Organization.objects.create(name="Org B")
    user = User.objects.create_user(username="user@example.com", password="StrongPass123!")
    OrganizationMembership.objects.create(user=user, organization=org_a, role=OrganizationRole.CEO)

    construction_a = Construction.objects.create(organization=org_a, name="Alpha Site")
    construction_b = Construction.objects.create(organization=org_b, name="Beta Site")

    Order.objects.create(construction=construction_a, name="Order A")
    Order.objects.create(construction=construction_b, name="Order B")

    client.login(username="user@example.com", password="StrongPass123!")
    response = client.get(reverse("construction:order-list"))

    orders = response.context["orders"]
    names = {order.name for order in orders}
    assert names == {"Order A"}


@pytest.mark.django_db
def test_contract_for_work_and_residuals_relationships():
    org = Organization.objects.create(name="Org A")
    construction = Construction.objects.create(organization=org, name="Alpha Site")
    order = Order.objects.create(construction=construction, name="Order A")

    contract = ContractForWork.objects.create(
        order=order,
        contract_number="CFW-001",
        contractor_share=12.5,
        day_after_due=10,
        warranty_period=24,
        is_social_house=False,
        tax_reverse_charge=True,
    )

    Residual.objects.create(contract_for_work=contract, percentage=5)

    assert order.contract == contract
    assert contract.residuals.count() == 1
