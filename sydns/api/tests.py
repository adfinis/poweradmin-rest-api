from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class DomainTests(APITestCase):

    fixtures = ['domains.yaml']

    def setUp(self):

        self.client.login(username='ldapuser', password='Test1234!')

    def test_domain_list_without_auth(self):

        client = APIClient()
        url = reverse('domain-list')
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_domain_list(self):

        url = reverse('domain-list')
        response = self.client.get(url, format='json')

        expected_json = {
            'results': [
                {'name': 'example.com',
                 'type': 'NATIVE',
                 'master': None}],
            'count': 1,
            'next': None,
            'previous': None}
        
        self.assertEqual(response.json() , expected_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_domain_retrieve(self):

        url = reverse('domain-list') + 'example.com/'
        response = self.client.get(url, format='json')

        expected_json = {'name': 'example.com',
                         'type': 'NATIVE',
                         'master': None}
        
        self.assertEqual(response.json() , expected_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
