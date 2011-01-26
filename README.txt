Flunc: a functional test suite runner for web applications.


Installation
============

We recommend installing into a Virtualenv_.

You should be able to install flunc by using ``easy_install flunc``; or 
you can download the tarball, extract, and run ``python setup.py develop``.  

Writing tests
=============

Flunc tests are Twill_ scripts.

There is a firefox extension that allows you to record tests directly
from within your browser. To install, visit

 * http://sourceforge.net/projects/testgen4web/

These tests are saved in an xml format. You can convert these tests
into a twill script by executing

 ``testgentotwill recorded.html > twillscript.twill``

Of course, you can still write tests manually.


Running tests
=============

Run ``flunc --help`` for details on running the functional tests.

By default flunc will search ./ftests/ to find tests. You can change
this with the ``-p`` (``--path``) option.

Some examples:

 ``flunc all``

runs all tests listed in all.tsuite against http://localhost/

 ``flunc -t http://localhost:8080/some_portal all``

runs all tests listed in all.tsuite against localhost:8080/some_portal

 ``flunc -c all create_user``

runs create_user.twill using all.conf

 ``flunc -c all create_user login create_project destroy_project destroy_user``

specify an ad hoc suite creating and tearing down a user and project
on default host

Finding tests
=============

Individual tests are contained in 

 <test>.twill 

A suite of tests are contained in 

 <suite>.tsuite 

Suite configurations are contained in

 <suite>.conf 

Cleanup suites are run after a suite, and are in

 <suite>_cleanup.tsuite

More details are on the `Flunc homepage`_.

.. _Virtualenv: http://pypi.python.org/pypi/virtualenv

.. _Twill: http://pypi.python.org/pypi/twill

.. _`Flunc homepage`: http://www.coactivate.org/projects/flunc

