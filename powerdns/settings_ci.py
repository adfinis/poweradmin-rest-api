from powerdns.settings import *  # noqa: F401

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'powerdns',
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
