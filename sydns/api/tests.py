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

        url = reverse('record-list') + '/1/'
        response = self.client.get(url, format='json')

        print(response.json())
        expected_json = {'content': 'dns1.syhosting.ch info@syhosting.ch 2014103002 ',
                         'ttl': 3600,
                         'domain_id': 1,
                         'id': 1,
                         'name': 'example.com',
                         'prio': 0,
                         'type': 'SOA'},

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

        expected_json = {'content': '192.168.3.4',
                'ttl': 3600,
                'domain_id': 1,
                'id': 5,
                'name': 'web01.example.com',
                'prio': 0,
                'type': 'A'}

        self.assertEqual(response.json() , expected_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # def test_record_destroy(self):

    #     url = reverse('record-detail')

    #     data = {'content': '192.168.3.3',
    #             'ttl': 3600,
    #             'domain_id': 1,
    #             'id': 1,
    #             'name': 'deleted.example.com',
    #             'prio': 0,
    #             'type': 'A'},

    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.json() , data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     response = self.client.delete(url + 'deleted.example.com/', data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
