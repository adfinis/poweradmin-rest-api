PowerDNS REST API
=================

|travis|

.. |travis|  image:: https://travis-ci.org/adfinis-sygroup/powerdns-rest-api.png?branch=master
   :target: https://travis-ci.org/adfinis-sygroup/powerdns-rest-api

A basic RESTful API for PowerDNS 3 compatible with PowerAdmin database schema.

Installation
------------
1. Install dependencies

.. code:: shell

    apt-get install python3 python3-pip python3-virtualenv virtualenv python3-dev libmysqlclient-dev libsasl2-dev libldap2-dev

2. Create and activate virtualenv

.. code:: shell

    virtualenv -p `which python3` env
    source env/bin/activate

3. Install python dependencies

.. code:: shell

    make install
    # or for development
    make install_dev


Settings
--------
Use `powerdns/settings_example.py` as basis for your configuration.

You can activate by using `DJANGO_SETTINGS_MODULE`

https://docs.djangoproject.com/en/1.11/topics/settings/#designating-the-settings

Documentation
-------------

You can browse the api with swagger by opening host name (e.g. http://localhost:8000).

For authentication use `api-token-auth` call and assign `username` and `password`.
You will receive a JWT token. Copy this token and click on `Authorize`.

As `api_key` assign `JWT token` and login. You should now see a `v1` api tree.

License
-------

PowerDNS REST API is licensed under GPL-3 or later following license model of PowerAdmin it is
based on.
