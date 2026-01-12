import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Organization

User = get_user_model()


@pytest.mark.django_db
def test_organization_scoped_redirects_anonymous(client):
    response = client.get(reverse("construction:construction-list"))
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@pytest.mark.django_db
def test_organization_scoped_requires_membership(client):
    user = User.objects.create_user(username="user@example.com", password="StrongPass123!")
    Organization.objects.create(name="Alpha Build")

    client.login(username="user@example.com", password="StrongPass123!")
    response = client.get(reverse("construction:construction-list"))
    assert response.status_code == 403
