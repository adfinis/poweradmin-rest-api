from rest_framework_jwt.test import APIJWTTestCase


class AuthTests(APIJWTTestCase):

    fixtures = ['domains.yaml']

    def test_ldap_auth(self):
        assert self.client.login(username='ldapuser', password='Test1234!')

    def test_ldap_auth_no_user_object(self):
        assert not self.client.login(
            username='ldapuser2', password='Test1234!'
        ), "User which is not in the user table should not be allowed to login"

    def test_model_auth(self):
        assert self.client.login(username='admin', password='Test1234!')

    def test_model_auth_invalid_user(self):
        assert not self.client.login(username='invalidadmin', password='t!')
