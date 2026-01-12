from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import BudgetItem, BudgetItemAmount, BudgetPeriod


def create_period(budget, created_by=None):
    if budget.periods.filter(status=BudgetPeriod.Status.OPEN).exists():
        raise ValidationError("An open period already exists.")
    return BudgetPeriod.objects.create(
        budget=budget,
        status=BudgetPeriod.Status.OPEN,
        created_by=created_by,
    )


def set_item_amount(period: BudgetPeriod, item: BudgetItem, amount: Decimal) -> BudgetItemAmount:
    if period.status != BudgetPeriod.Status.OPEN:
        raise ValidationError("Amounts can only be updated for an open period.")
    if period.created_at is None:
        raise ValidationError("Period must be saved before adding amounts.")

    obj, _created = BudgetItemAmount.objects.get_or_create(period=period, budget_item=item)
    obj.amount = amount
    obj.full_clean()
    obj.save()
    return obj


def submit_period(period: BudgetPeriod) -> BudgetPeriod:
    if period.status != BudgetPeriod.Status.OPEN:
        raise ValidationError("Only open periods can be submitted.")
    period.status = BudgetPeriod.Status.SUBMITTED
    period.submitted_at = timezone.now()
    period.save(update_fields=["status", "submitted_at"])
    return period


def accept_period(period: BudgetPeriod) -> BudgetPeriod:
    if period.status != BudgetPeriod.Status.SUBMITTED:
        raise ValidationError("Only submitted periods can be accepted.")
    period.status = BudgetPeriod.Status.ACCEPTED
    period.reviewed_at = timezone.now()
    period.save(update_fields=["status", "reviewed_at"])
    return period


def decline_period(
    period: BudgetPeriod,
    payment: Decimal | None = None,
    penalty: Decimal | None = None,
    fee: Decimal | None = None,
) -> BudgetPeriod:
    if period.status != BudgetPeriod.Status.SUBMITTED:
        raise ValidationError("Only submitted periods can be declined.")
    period.status = BudgetPeriod.Status.OPEN
    period.reviewed_at = timezone.now()
    period.decline_payment = payment
    period.decline_penalty = penalty
    period.decline_fee = fee
    period.save(update_fields=["status", "reviewed_at", "decline_payment", "decline_penalty", "decline_fee"])
    return period


def close_period(period: BudgetPeriod) -> BudgetPeriod:
    if period.status != BudgetPeriod.Status.ACCEPTED:
        raise ValidationError("Only accepted periods can be closed.")
    period.status = BudgetPeriod.Status.CLOSED
    period.closed_at = timezone.now()
    period.save(update_fields=["status", "closed_at"])
    return period
