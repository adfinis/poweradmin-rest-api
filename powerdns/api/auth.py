from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django_auth_ldap.backend import LDAPBackend, _LDAPUser

UserModel = get_user_model()


class ModelBackend(ModelBackend):
    """
    Authenticates against powerdns.api.User model

    Only authenticates against password in database if use_ldap
    flag is set to zero.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:  # pragma: no cover
            username = kwargs.get(UserModel.USERNAME_FIELD)

        user = UserModel.objects.filter(
            username__iexact=username, use_ldap=0, is_active=True).first()
        if user is None or not user.check_password(password):
            return None

        return user


class LDAPBackend(LDAPBackend):
    """
    Authenticated against ldap

    Added ability that only users with use_ldap flag set to
    one can actually authenticate.
    """
    def authenticate(self, request, username, password, **kwargs):
        """
        To suppress RemovedInDjango21Warning added function with first argument
        being request. Can be removed once
        https://bitbucket.org/psagers/django-auth-ldap/issues/73 is fixed.
        """
        return super().authenticate(username, password, **kwargs)

    def get_or_create_user(self, username, ldap_user):
        """
        Users which do not exist on database with flag use_ldap=1
        are not allowed to login. Hence, we do not create users
        but throw an authentication failed exception to stop authentication
        process.
        """
        model = self.get_user_model()

        try:
            return (
                model.objects.get(username__iexact=username, use_ldap=1), False
            )
        except model.DoesNotExist:
            raise _LDAPUser.AuthenticationFailed(
                "User %s doesn't exist in user table" % username
            )
