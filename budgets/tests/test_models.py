import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import Organization
from budgets.models import (
    Budget,
    BudgetHeader,
    BudgetItem,
    BudgetItemAmount,
    BudgetPeriod,
)
from construction.models import Construction, Order

User = get_user_model()


def build_budget():
    organization = Organization.objects.create(name="Org A")
    construction = Construction.objects.create(organization=organization, name="Site A")
    order = Order.objects.create(construction=construction, name="Order A")
    budget = Budget.objects.create(order=order, name="Rozpocet A")
    return budget


@pytest.mark.django_db
def test_only_one_open_period_per_budget():
    budget = build_budget()
    BudgetPeriod.objects.create(budget=budget, status=BudgetPeriod.Status.OPEN)

    with pytest.raises(IntegrityError):
        BudgetPeriod.objects.create(budget=budget, status=BudgetPeriod.Status.OPEN)


@pytest.mark.django_db
def test_budget_item_amount_unique_per_period():
    budget = build_budget()
    header = BudgetHeader.objects.create(budget=budget, title="Header")
    item = BudgetItem.objects.create(
        header=header,
        code="001",
        description="Item",
        measure_unit="m2",
        price_for_unit="10.50",
    )
    period = BudgetPeriod.objects.create(budget=budget, status=BudgetPeriod.Status.OPEN)

    BudgetItemAmount.objects.create(period=period, budget_item=item, amount="100.00")

    with pytest.raises(IntegrityError):
        BudgetItemAmount.objects.create(period=period, budget_item=item, amount="50.00")


@pytest.mark.django_db
def test_budget_item_belongs_to_header_budget():
    budget = build_budget()
    other_budget = build_budget()
    header = BudgetHeader.objects.create(budget=budget, title="Header")

    item = BudgetItem.objects.create(
        header=header,
        code="002",
        description="Item",
        measure_unit="ks",
        price_for_unit="1.00",
    )

    assert item.header.budget_id == budget.id
    assert item.header.budget_id != other_budget.id
