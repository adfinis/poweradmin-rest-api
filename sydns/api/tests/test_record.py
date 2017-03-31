from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class RecordTests(APITestCase):

    fixtures = ['domains.yaml']

    def setUp(self):

        self.client.login(username='ldapuser', password='Test1234!')

    def test_record_list_without_auth(self):

        client = APIClient()
        url = reverse('record-list')
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_record_list(self):

        url = reverse('record-list')
        response = self.client.get(url, format='json')

        expected_json = {'previous': None,
                         'next': None,
                         'results': [
                             {'content': 'dns1.syhosting.ch info@syhosting.ch 2014103002 ','ttl': 3600, 'domain_id': 1, 'id': 1, 'name': 'example.com', 'prio': 0, 'type': 'SOA'},
                             {'content': 'dns1.syhosting.ch', 'ttl': 3600, 'domain_id': 1, 'id': 2, 'name': 'example.com', 'prio': 0, 'type': 'NS'},
                             {'content': 'dns2.syhosting.ch', 'ttl': 3600, 'domain_id': 1, 'id': 3, 'name': 'example.com', 'prio': 0, 'type': 'NS'},
                             {'content': '91.234.189.11', 'ttl': 600, 'domain_id': 1, 'id': 4, 'name': 'www.example.com', 'prio': 0, 'type': 'A'}],
                         'count': 4}

        self.assertEqual(response.json() , expected_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_record_retrieve(self):

        url = reverse('record-detail', args=[1])

        response = self.client.get(url, format='json')

        expected_json = {'content': 'dns1.syhosting.ch info@syhosting.ch 2014103002 ',
                         'ttl': 3600,
                         'domain_id': 1,
                         'id': 1,
                         'name': 'example.com',
                         'prio': 0,
                         'type': 'SOA'}

        self.assertEqual(response.json() , expected_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_record_create(self):

        url = reverse('record-list')

        data = {'content': '192.168.3.4',
                'ttl': 3600,
                'domain_id': 1,
                'name': 'web01.example.com',
                'prio': 0,
                'type': 'A'}

        response = self.client.post(url, data, format='json')

        returned_data = response.json()

        # Remove primary key from data
        returned_data.pop('id')

        self.assertEqual(returned_data , data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_record_destroy(self):

        url = reverse('record-detail', args=[1])

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
