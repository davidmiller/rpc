.. RPC documentation master file, created by
   sphinx-quickstart on Mon Mar 19 20:29:35 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to RPC's documentation!
===============================

Rpc gives you a consistent API for RPC protocols that doesn't suck!

Because you too can have nice things::

    from rpc import thrifty

    import Service

    with thrifty.client("localhost:45678", Service) as c:
        print c.ping()

`See the same code`_ the way the Thrift documentation would have you do it.

.. _See the same code: https://gist.github.com/2127419

Nobody likes writing boilerplate code - so stop writing it!

.. _protocols:

Supported Protocols
-------------------

* :ref:`rpc.jsonrpc`
* :ref:`rpc.jsonp`
* :ref:`rpc.thrifty`

Clients
-------

Rpc makes creating clients easy - contextmanagers where you have to keep track of connections, and class factories for places where that doesn't matter.

:ref:`clients`

Servers
-------

By abstracting away the mechanics of associating your function handlers from protocol specific code, RPC allpows you an easy way to create RPC servers, and makes serving to multiple protocols so much easier.

:ref:`servers`

API Docs
--------

.. toctree::
   :maxdepth: 1

   modules/chain
   modules/clients
   modules/exceptions
   modules/jsonp
   modules/jsonrpc
   modules/servers
   modules/thrifty

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
