Supah simple sms handler
=======================

.. contents::
   :local:
   :depth: 2

Purpose
-------
It's small and simple test project that implements

- base way to configure similar sms providers api gates
- unified sms logging
- sms handler register set for simple use

.. note::

    If you're casual traveller, use this project as education-only way purpose.

Installation
------------

.. code-block:: bash

   python setup.py install

No pypi build though as this project is not yet for any production purpose

Use
---

.. code-block:: python

    from sms import base

    class MyProvider(base.BaseSMSHandler):
        SEND_MESSAGE_URL = 'http://your-provider-url.com/sms/send-message/'

        #: required
        def get_send_message_post_data(self, request):
            return {
                'text': request.message,
                'number': request.phone
            }

        #: optional if you have authorization process via headers
        def get_send_message_headers(self):
            return {'api-key': '<your secret api key>'}
    
    #: if authentication data is given via POST params
    handler = MyProvider(auth_credentials={'user': 'user', 'api-key': 'api-key'})
    #: phone is not real
    handler.send('message', '79110000102')

Testing
-------

With help of `tox <http://tox.testrun.org/>`_

.. code-block:: bash

   user@localhost simple-sms-handler$ tox

With help of ``setup.py``

.. code-block:: bash

   user@localhost simple-sms-handler$ python setup.py test


Without any help (you should install requirements first though, use  ``django_app/requirements/base.txt``)

.. code-block:: bash

   user@localhost simple-sms-handler$ python -m unittest test.test_handlers

Django app
----------
Django app is a simple way to represent how to log sms messages with help of django orm and python logging

Requirements
~~~~~~~~~~~~

Install manually

- django==1.9rc1
- requests==2.8.1
- wheel==0.24.0

or with using pip:

.. code-block:: bash

   user@localhost simple-sms-handler$ pip install -r django_app/requirements/base.txt

Testing
~~~~~~~
Simply run

.. code-block:: bash

   user@localhost django_app$ ./run_tests.sh

.. note::
   
   Django app uses globaly configurated sms gate (which one basicly is fake), so if there're any
   errors/failures inside that tests. Apply uncomment responses decorator inside django_app/apps/sms/tests.py file
   every test you can find there.

