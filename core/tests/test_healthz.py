import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_healthz_endpoint(client):
    response = client.get(reverse("healthz"))
    assert response.status_code == 200
    assert response.content == b"ok"
