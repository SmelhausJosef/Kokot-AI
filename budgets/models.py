from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from construction.models import Order


class Budget(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="budgets")
    name = models.CharField(max_length=200)
    excel_file = models.FileField(upload_to="budgets/excel/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class BudgetHeader(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="headers")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class BudgetItem(models.Model):
    header = models.ForeignKey(BudgetHeader, on_delete=models.CASCADE, related_name="items")
    code = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    measure_unit = models.CharField(max_length=50, blank=True)
    price_for_unit = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["code", "description"]

    def __str__(self) -> str:
        return f"{self.code} {self.description}".strip()


class BudgetPeriod(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        SUBMITTED = "submitted", "Submitted"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"
        CLOSED = "closed", "Closed"

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="periods")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="budget_periods"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    decline_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    decline_penalty = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    decline_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["budget"],
                condition=Q(status="open"),
                name="unique_open_period_per_budget",
            )
        ]

    def __str__(self) -> str:
        return f"{self.budget} ({self.status})"


class BudgetItemAmount(models.Model):
    period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE, related_name="item_amounts")
    budget_item = models.ForeignKey(BudgetItem, on_delete=models.CASCADE, related_name="period_amounts")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["period", "budget_item"],
                name="unique_amount_per_item_period",
            )
        ]

    def __str__(self) -> str:
        return f"{self.budget_item} ({self.amount})"

    def clean(self):
        if self.amount is not None and self.amount < 0:
            raise ValidationError("Amount must be non-negative.")
        if self.period_id and self.budget_item_id:
            if self.period.budget_id != self.budget_item.header.budget_id:
                raise ValidationError("Budget item does not belong to the same budget as period.")

            if self.period.created_at:
                previous_amount = (
                    BudgetItemAmount.objects.filter(
                        budget_item=self.budget_item,
                        period__budget=self.period.budget,
                        period__created_at__lt=self.period.created_at,
                    )
                    .order_by("-period__created_at")
                    .values_list("amount", flat=True)
                    .first()
                )
                if previous_amount is not None and self.amount < previous_amount:
                    raise ValidationError("Amount cannot be lower than previous period.")
