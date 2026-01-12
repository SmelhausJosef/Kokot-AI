from accounts.models import OrganizationMembership
from accounts.services import normalize_role


def current_membership(request):
    if not request.user.is_authenticated:
        return {}

    membership = (
        OrganizationMembership.objects.select_related("organization")
        .filter(user=request.user)
        .first()
    )
    if not membership:
        return {}

    role = normalize_role(membership.role)
    return {
        "active_membership": membership,
        "active_organization": membership.organization,
        "active_role": role,
    }
