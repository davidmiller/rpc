Rpc gives you a consistent API for RPC protocols that doesn't suck!

Because you too can have nice things

::

    >>> from rpc import thrifty
    >>> import Service
    >>> with thrifty.client("localhost:45678", Service) as c:
    ...     print c.ping()

Check out the documentation: http://www.deadpansincerity.com/docs/rpc

.. image:: https://secure.travis-ci.org/davidmiller/rpc.png?branch=master
   :alt: Build Status
   :target: https://secure.travis-ci.org/davidmiller/rpc
