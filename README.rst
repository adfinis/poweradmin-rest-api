SyDNS
=====
A basic RESTful API for PowerDNS 3

Installation
------------
1. Install dependencies

.. code:: shell

    apt-get install python3 python3-pip python3-dev libmysqlclient-dev

2. Create and activate virtualenv

.. code:: shell

    virtualenv -p `which python3` env
    source env/bin/activate

3. Install python dependencies

    pip install -r requirements.txt
   

PowerDNS SQL Schema Adjustments
-------------------------------
Our current PowerDNS schema does not use constraints to prevent orphan records.
Checkout `sample/patched_database_schema.sql` for further information.


	  
