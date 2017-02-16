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
            'results': [{'name': 'example.com',
                         'type': 'NATIVE'}],
            'count': 1,
            'next': None,
            'previous': None}

        self.assertEqual(response.json() , expected_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_domain_retrieve(self):

        url = reverse('domain-list') + 'example.com/'

        response = self.client.get(url, format='json')

        expected_json = {'name': 'example.com',
                         'type': 'NATIVE'}

        self.assertEqual(response.json() , expected_json)

    def test_domain_create(self):

        url = reverse('domain-list')

        data = {'name': 'test-example.com',
                'type': 'NATIVE'}


        response = self.client.post(url, data, format='json')

        self.assertEqual(response.json() , data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_domain_update(self):

        url = reverse('domain-list') + 'example.com/'

        data = {'name': 'example2.com',
                'type': 'NATIVE'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.json() , data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_domain_destroy(self):

        url = reverse('domain-list')

        data = {'name': 'to-be-deleted-example.com',
                'type': 'NATIVE'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.json() , data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(url + 'to-be-deleted-example.com/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
