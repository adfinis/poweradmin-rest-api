import pytest
import mockldap


@pytest.fixture(autouse=True, scope="session")
def managed_models():
    """
    For unit tests we need create an empty powerdns database
    scheme but this only works for models which are managed.
    Hence with this auto fixture we temporarly change models to be managed.
    """
    from django.apps import apps
    app = apps.get_app_config('api')
    unmanaged_models = list(app.get_models())
    for model in unmanaged_models:
        model._meta.managed = True

    yield

    unmanaged_models = list(app.get_models())
    for model in unmanaged_models:
        model._meta.managed = False


@pytest.fixture(autouse=True, scope="session")
def ldap_users():
    top = ("o=test", {"o": "test"})
    people = ("ou=people,o=test", {"ou": "people"})
    groups = ("ou=groups,o=test", {"ou": "groups"})

    ldapuser = (
        "uid=ldapuser,ou=people,o=test", {
            "uid": ["ldapuser"],
            "objectClass": [
                "person", "organizationalPerson",
                "inetOrgPerson", "posixAccount"
            ],
            "userPassword": ["Test1234!"],
            "uidNumber": ["1000"],
            "gidNumber": ["1000"],
            "givenName": ["Ldapuser"],
            "sn": ["LdapUser"]
        }
    )
    directory = dict([top, people, groups, ldapuser])  # noqa: C406

    mock = mockldap.MockLdap(directory)
    mock.start()

    yield

    mock.stop()
    del mock
