from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .models import OrganizationMembership, OrganizationRole

User = get_user_model()


def get_active_membership(user) -> OrganizationMembership:
    membership = OrganizationMembership.objects.select_related("organization").filter(user=user).first()
    if not membership:
        raise PermissionDenied("User has no organization membership.")
    return membership


def get_construction_manager_queryset(organization):
    roles = [
        OrganizationRole.CONSTRUCTION_MANAGER,
        OrganizationRole.SUB_CONSTRUCTION_MANAGER,
    ]
    return User.objects.filter(memberships__organization=organization, memberships__role__in=roles).distinct()
