Flunc: a functional test suite runner.

Writing tests
=============

You should be able to ``python setup.py develop`` into a workingenv
or virtualenv; after that ...

There is a firefox extension that allows you to record tests directly
from within your browser. To install, visit

 * http://developer.spikesource.com/wiki/index.php/Projects:TestGen4Web

These tests are saved in an xml format. You can convert these tests
into a twill script by executing

 ``testgentotwill recorded.html > twillscript.twill``

Of course, you can still write tests manually. The individual tests
are themselves twill scripts.

Running tests
=============

Run ``flunc --help`` for details on running the functional tests.

By default flunc will search ./ftests/ to find tests. You can change
this with the ``-p`` (``--path``) option.

 ``flunc all``

runs all tests listed in all.tsuite against localhost:8080/openplans

 ``flunc -t http://localhost:8080/some_portal all``

runs all tests listed in all.tsuite against localhost:8080/some_portal

 ``flunc -t http://localhost:8080/p -c all create_user``

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
