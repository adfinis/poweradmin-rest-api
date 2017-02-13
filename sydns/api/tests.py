from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class DomainTests(APITestCase):

    fixtures = ['domains.yaml']

    def setUp(self):

        self.noauth_client = APIClient()
        self.client.login(username='ldapuser', password='Test1234!')

    def test_domain_list(self):

        url = reverse('domain-list')

        auth_response = self.client.get(url)
        noauth_response = self.client.get(url)

        self.assertEqual auth_response.status_code == status.HTTP_200_OK
        self.assertEqual noauth_response.status_code == status.HTTP_401_UNAUTHORIZED
