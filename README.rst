py-xmlasdict
===================================

python library to read xml DOM trees as dicts (with iter and gettattribute behaviour)

Started on 2022-02-01

Setup
-----
Start using this project in a virtual environment

.. code-block:: bash

    $ virtualenv venv
    $ source venv/Scripts/activate
    $ pip install -r requirements.txt

Initialize to grab dependencies

.. code-block:: bash

    $ make init       # install dependencies
    $ make init-dev   # includes the previous + adds dependencies for developers

Build Docs

.. code-block:: bash

    $ make docu



Developers
----------

Run Tests

.. code-block:: bash

    $ make test                                                   # to run all tests
    $ PYTEST_LOGCONF=debug-logconf.yml python tests/test_demo.py  # to run a specific test with specific logging


Check the code-style and syntax (flake8)

.. code-block:: bash

    $ make check
