from powerdns.settings import *  # noqa: F401

# needs to OFF in production
DEBUG = False

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'powerdns',
        'USER': 'powerdns',
        'PASSWORD': 'somepasword',
        'HOST': 'mysql',
        'PORT': '3306',
    }
}

# ldap configuration
LDAP_BASE = 'dc=example,dc=com'
AUTH_LDAP_SERVER_URI = "ldaps://localhost:7636"
AUTH_LDAP_BIND_DN = 'uid=powerdns.ldap.auth,cn=users,{}'.format(LDAP_BASE)
AUTH_LDAP_START_TLS = False
AUTH_LDAP_BIND_PASSWORD = 'somepassword'
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,cn=users,{0}'.format(LDAP_BASE)

# add some random string
# see http://oonlab.com/edx/django/python/2016/08/09/generate-secret-key-django
SECRET_KEY = ''

# list of hosts which are allowed to connect to this service
ALLOWED_HOSTS = []
