import uuid
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from accounts.models import Invitation, Organization, OrganizationMembership, OrganizationRole

User = get_user_model()


@pytest.mark.django_db
def test_public_registration_creates_org_and_ceo_membership(client):
    payload = {
        "email": "ceo@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
        "organization_name": "Alpha Build",
    }
    response = client.post(reverse("accounts:register"), payload)
    assert response.status_code == 302

    user = User.objects.get(username="ceo@example.com")
    organization = Organization.objects.get(name="Alpha Build")
    membership = OrganizationMembership.objects.get(user=user, organization=organization)
    assert membership.role == OrganizationRole.CEO


@pytest.mark.django_db
def test_invite_registration_requires_valid_token(client):
    bad_token = uuid.uuid4()
    response = client.get(reverse("accounts:invite-register", args=[bad_token]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_invite_registration_rejects_expired_invitation(client):
    inviter = User.objects.create_user(username="ceo@example.com", password="StrongPass123!")
    organization = Organization.objects.create(name="Delta Works")
    invitation = Invitation.objects.create(
        organization=organization,
        email="manager@example.com",
        role=OrganizationRole.BUDGET_MANAGER,
        invited_by=inviter,
        expires_at=timezone.now() - timedelta(days=1),
    )

    response = client.get(reverse("accounts:invite-register", args=[invitation.token]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_invite_registration_rejects_accepted_invitation(client):
    inviter = User.objects.create_user(username="ceo@example.com", password="StrongPass123!")
    organization = Organization.objects.create(name="Delta Works")
    invitation = Invitation.objects.create(
        organization=organization,
        email="manager@example.com",
        role=OrganizationRole.BUDGET_MANAGER,
        invited_by=inviter,
        accepted_at=timezone.now(),
    )

    response = client.get(reverse("accounts:invite-register", args=[invitation.token]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_invite_registration_creates_membership_and_marks_accepted(client):
    inviter = User.objects.create_user(username="ceo@example.com", password="StrongPass123!")
    organization = Organization.objects.create(name="Delta Works")
    invitation = Invitation.objects.create(
        organization=organization,
        email="manager@example.com",
        role=OrganizationRole.BUDGET_MANAGER,
        invited_by=inviter,
    )

    payload = {
        "email": "manager@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    }
    response = client.post(reverse("accounts:invite-register", args=[invitation.token]), payload)
    assert response.status_code == 302

    user = User.objects.get(username="manager@example.com")
    membership = OrganizationMembership.objects.get(user=user, organization=organization)
    assert membership.role == OrganizationRole.BUDGET_MANAGER

    invitation.refresh_from_db()
    assert invitation.accepted_at is not None
