import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_frontend_backend_health():
    client = APIClient()
    url = reverse('frontend_backend_health')
    response = client.get(url)
    assert response.status_code == 200
