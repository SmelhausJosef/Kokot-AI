from decimal import Decimal

from django.conf import settings
from django.db import models

from accounts.models import Organization


class Construction(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="constructions")
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE, related_name="orders")
    name = models.CharField(max_length=200)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="managed_orders")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ContractForWork(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="contract")
    contract_number = models.CharField(max_length=100)
    contractor_share = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    contract_signed = models.DateTimeField(null=True, blank=True)
    day_after_due = models.IntegerField(default=0)
    end_contract = models.DateField(null=True, blank=True)
    is_social_house = models.BooleanField(default=False)
    start_contract = models.DateField(null=True, blank=True)
    tax_reverse_charge = models.BooleanField(default=False)
    warranty_period = models.IntegerField(default=0)

    class Meta:
        ordering = ["contract_number"]

    def __str__(self) -> str:
        return self.contract_number


class Residual(models.Model):
    contract_for_work = models.ForeignKey(
        ContractForWork, on_delete=models.CASCADE, related_name="residuals"
    )
    end_date = models.DateField(null=True, blank=True)
    percentage = models.IntegerField()

    class Meta:
        ordering = ["end_date"]

    def __str__(self) -> str:
        return f"{self.percentage}%"

# Create your models here.
