import pytest
from django.core.exceptions import ValidationError

from accounts.models import Organization
from budgets.models import BudgetHeader, BudgetItem
from budgets.services import (
    accept_period,
    close_period,
    create_period,
    decline_period,
    set_item_amount,
    submit_period,
)
from construction.models import Construction, Order


def build_budget():
    organization = Organization.objects.create(name="Org A")
    construction = Construction.objects.create(organization=organization, name="Site A")
    order = Order.objects.create(construction=construction, name="Order A")
    return order.budgets.create(name="Rozpocet A")


def build_item(budget):
    header = BudgetHeader.objects.create(budget=budget, title="Header")
    return BudgetItem.objects.create(
        header=header,
        code="001",
        description="Item",
        measure_unit="m2",
        price_for_unit="10.50",
    )


@pytest.mark.django_db
def test_submit_accept_close_flow():
    budget = build_budget()
    period = create_period(budget)

    submit_period(period)
    assert period.status == period.Status.SUBMITTED
    assert period.submitted_at is not None

    accept_period(period)
    assert period.status == period.Status.ACCEPTED
    assert period.reviewed_at is not None

    close_period(period)
    assert period.status == period.Status.CLOSED
    assert period.closed_at is not None


@pytest.mark.django_db
def test_decline_returns_to_open_with_fees():
    budget = build_budget()
    period = create_period(budget)

    submit_period(period)
    period = decline_period(period, payment="100.00", penalty="10.00", fee="5.00")

    assert period.status == period.Status.OPEN
    assert period.reviewed_at is not None
    assert str(period.decline_payment) == "100.00"
    assert str(period.decline_penalty) == "10.00"
    assert str(period.decline_fee) == "5.00"


@pytest.mark.django_db
def test_create_period_only_one_open():
    budget = build_budget()
    create_period(budget)

    with pytest.raises(ValidationError):
        create_period(budget)


@pytest.mark.django_db
def test_set_item_amount_requires_open_period():
    budget = build_budget()
    item = build_item(budget)
    period = create_period(budget)

    submit_period(period)

    with pytest.raises(ValidationError):
        set_item_amount(period, item, "10.00")


@pytest.mark.django_db
def test_set_item_amount_validates_previous_period():
    budget = build_budget()
    item = build_item(budget)

    period_one = create_period(budget)
    set_item_amount(period_one, item, "100.00")
    submit_period(period_one)
    accept_period(period_one)
    close_period(period_one)

    period_two = create_period(budget)

    with pytest.raises(ValidationError):
        set_item_amount(period_two, item, "50.00")

    amount = set_item_amount(period_two, item, "150.00")
    assert str(amount.amount) == "150.00"


@pytest.mark.django_db
def test_decline_fails_if_another_open_period_exists():
    budget = build_budget()
    period_one = create_period(budget)
    submit_period(period_one)

    period_two = create_period(budget)

    with pytest.raises(ValidationError):
        decline_period(period_one)

    assert period_two.status == period_two.Status.OPEN
