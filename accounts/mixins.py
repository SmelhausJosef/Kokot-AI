from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

from accounts.services import get_active_membership, normalize_role


class OrganizationScopedMixin(AccessMixin):
    membership = None
    organization = None

    def setup_membership(self, request):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.membership = get_active_membership(request.user)
        self.organization = self.membership.organization
        return None

    def dispatch(self, request, *args, **kwargs):
        if self.membership is None:
            response = self.setup_membership(request)
            if response is not None:
                return response
        return self.dispatch_with_membership(request, *args, **kwargs)

    def dispatch_with_membership(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RoleRequiredMixin(OrganizationScopedMixin):
    required_roles = set()

    def dispatch(self, request, *args, **kwargs):
        response = self.setup_membership(request)
        if response is not None:
            return response
        if self.required_roles:
            role = normalize_role(self.membership.role)
            if role not in self.required_roles:
                raise PermissionDenied("User role is not allowed for this action.")
        return self.dispatch_with_membership(request, *args, **kwargs)
