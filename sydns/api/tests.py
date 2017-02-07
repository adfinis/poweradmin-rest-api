from django.core.urlresolvers import reverse
from api.models import Domain
from rest_framework.test import APITestCase
from rest_framework import status


class DomainTests(APITestCase):

    def test_domain_list(self):
        url = reverse('domain-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

