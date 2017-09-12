from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework_jwt.test import APIJWTTestCase

from powerdns.api import models


class RecordTests(APIJWTTestCase):
    # TODO: use pure pytest and fixtures
    # this will also replace django fixtures which are hard to maintain

    fixtures = ['domains.yaml']

    def setUp(self):
        self.client.login(username='ldapuser', password='Test1234!')

    def test_record_list_without_auth(self):
        self.client.logout()
        url = reverse('record-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_record_list_without_domain_filter(self):
        url = reverse('record-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_record_list(self):

        url = reverse('record-list')
        response = self.client.get(
            url, format='json', data={'domain': 'example.com'}
        )

        expected_json = {
            'previous': None,
            'next': None,
            'results': [
                {'content': 'dns1.syhosting.ch info@syhosting.ch 2014103002 ',
                 'ttl': 3600,
                 'domain': 'example.com',
                 'id': 1,
                 'name': 'example.com',
                 'prio': 0,
                 'type': 'SOA'},
                {'content': 'dns1.syhosting.ch',
                 'ttl': 3600,
                 'domain': 'example.com',
                 'id': 2,
                 'name': 'example.com',
                 'prio': 0,
                 'type': 'NS'},
                {'content': 'dns2.syhosting.ch',
                 'ttl': 3600,
                 'domain': 'example.com',
                 'id': 3,
                 'name': 'example.com',
                 'prio': 0,
                 'type': 'NS'},
                {'content': '93.184.216.34',
                 'ttl': 600,
                 'domain': 'example.com',
                 'id': 4,
                 'name': 'www.example.com',
                 'prio': 0,
                 'type': 'A'}
            ],
            'count': 4
        }

        assert response.json() == expected_json
        assert response.status_code == status.HTTP_200_OK

    def test_record_retrieve(self):

        url = reverse('record-detail', args=[1])

        response = self.client.get(url, format='json')

        expected_json = {
            'content': 'dns1.syhosting.ch info@syhosting.ch 2014103002 ',
            'ttl': 3600,
            'domain': 'example.com',
            'id': 1,
            'name': 'example.com',
            'prio': 0,
            'type': 'SOA'}

        assert response.json() == expected_json
        assert response.status_code == status.HTTP_200_OK

    def test_record_create(self):

        url = reverse('record-list')

        data = {'content': '192.168.3.4',
                'ttl': 3600,
                'domain': 'example.com',
                'name': 'web01.example.com',
                'prio': 0,
                'type': 'A'}

        response = self.client.post(url, data, format='json')

        returned_data = response.json()

        # Remove primary key from data
        returned_data.pop('id')

        self.assertEqual(returned_data , data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_record_create_foreign_domain(self):
        url = reverse('record-list')

        models.Zone.objects.filter(domain__name='example.com').delete()

        data = {'content': '192.168.3.4',
                'ttl': 3600,
                'domain': 'example.com',
                'name': 'web01.example.com',
                'prio': 0,
                'type': 'A'}

        response = self.client.post(url, data, format='json')
        assert response.status_code == 403

    def test_record_destroy(self):

        url = reverse('record-detail', args=[1])

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
