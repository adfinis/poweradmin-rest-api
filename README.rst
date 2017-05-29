SyDNS
=====
A basic RESTful API for PowerDNS 3

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

    pip install -r requirements.txt


Configuration
-------------
The configuration happens through `sydns/configuration.py`.


TODO: how to test with real data
