from powerdns.settings import *  # noqa: F401


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'powerdns',
        'USER': 'powerdns',
        'PASSWORD': 'powerdns',
        'HOST': 'mysql',
        'PORT': '3306',
    }
}
