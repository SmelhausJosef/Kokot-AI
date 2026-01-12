from django.db import transaction
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import InviteSignupForm, PublicSignupForm
from .models import Invitation, Organization, OrganizationMembership, OrganizationRole


class PublicSignupView(FormView):
    template_name = "accounts/register.html"
    form_class = PublicSignupForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            organization = Organization.objects.create(name=form.cleaned_data["organization_name"])
            OrganizationMembership.objects.create(
                user=user,
                organization=organization,
                role=OrganizationRole.CEO,
            )
        return super().form_valid(form)


class InviteSignupView(FormView):
    template_name = "accounts/invite_register.html"
    form_class = InviteSignupForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        self.invitation = self._get_invitation()
        return super().dispatch(request, *args, **kwargs)

    def _get_invitation(self) -> Invitation:
        token = self.kwargs.get("token")
        try:
            invitation = Invitation.objects.select_related("organization").get(token=token)
        except Invitation.DoesNotExist as exc:
            raise Http404 from exc
        if invitation.is_expired or invitation.is_accepted:
            raise Http404
        return invitation

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["invitation"] = self.invitation
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            invitation = self._get_invitation_for_update()
            user = form.save()
            OrganizationMembership.objects.create(
                user=user,
                organization=invitation.organization,
                role=invitation.role,
            )
            invitation.mark_accepted()
        return super().form_valid(form)

    def _get_invitation_for_update(self) -> Invitation:
        token = self.kwargs.get("token")
        try:
            invitation = (
                Invitation.objects.select_for_update()
                .select_related("organization")
                .get(token=token)
            )
        except Invitation.DoesNotExist as exc:
            raise Http404 from exc
        if invitation.is_expired or invitation.is_accepted:
            raise Http404
        return invitation
