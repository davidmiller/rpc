.. _clients:

RPC Clients
===========

Initialising an RPC client shouldn't be that hard.

RPC provides a consistent API across protocols.

An example
----------

Let's say we want to connect to a JSON RPC server. The code for doing so is trivial::

    from rpc.jsonrpc import Client

    client = Client("http://localhost:6789")

    print client.ping()

That's all there is to it.

Well... Some protocols make it slightly harder, but you should probably consult the :ref:`protocols` documentation for details...

Contextmanagers
---------------

All the rpc clients also work as contextmanagers. For protocols where you have to take care of closing connections, this can be quite a help::

    from rpc.jsonrpc import Client

    with Client("localhost",6789") as client:
        print client.ping()

Protocol Classes
----------------

Some protocols need a Python class to function, that's fine. With Rpc it's the third argument::

    from rpc import thrifty

    import Service

    with thrifty.client("localhost", 45678, Service) as c:
        print c.ping()

Opening and closing connections
-------------------------------

For protocols that require an explicit open/close of some connection, the client will provide a `.close()` method::

    from rpc import thrifty

    import Service

    c.client("localhost", 45678, Service)
        print c.ping()

Chaining
--------

Sometimes you need access to a bunch of services all at once. The chain API makes this easy::

    from rpc.jsonrpc import chain

    one, two = chain(("http://localhost:7890").chain("http://localhost:7890", timeout=5, verb="GET"))