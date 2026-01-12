from datetime import timedelta
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Organization(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcontractors",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    @property
    def is_subcontractor(self) -> bool:
        return self.parent_id is not None


class OrganizationRole(models.TextChoices):
    CEO = "CEO", "CEO"
    ACCOUNT_MANAGER = "ACCOUNT_MANAGER", "Account Manager"
    BUDGET_MANAGER = "BUDGET_MANAGER", "Budget Manager"
    CONSTRUCTION_MANAGER = "CONSTRUCTION_MANAGER", "Construction Manager"
    SUBCEO = "SUBCEO", "Sub CEO"
    SUB_ACCOUNT_MANAGER = "SUB_ACCOUNT_MANAGER", "Sub Account Manager"
    SUB_BUDGET_MANAGER = "SUB_BUDGET_MANAGER", "Sub Budget Manager"
    SUB_CONSTRUCTION_MANAGER = "SUB_CONSTRUCTION_MANAGER", "Sub Construction Manager"


class OrganizationMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=40, choices=OrganizationRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self) -> str:
        return f"{self.user} -> {self.organization} ({self.role})"


def default_invitation_expiry():
    return timezone.now() + timedelta(days=7)


class Invitation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    role = models.CharField(max_length=40, choices=OrganizationRole.choices)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_invitations"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_invitation_expiry)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["token"])]

    def __str__(self) -> str:
        return f"{self.email} ({self.organization})"

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_accepted(self) -> bool:
        return self.accepted_at is not None

    def mark_accepted(self) -> None:
        self.accepted_at = timezone.now()
        self.save(update_fields=["accepted_at"])

# Create your models here.
