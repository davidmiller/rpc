.. _servers:

RPC Servers
===========

RPC has a consistent metaphor for writing RPC servers. You define a handler class that contains your API endpoints, and you pass this to a server class which initialises for you.

RPC will provide you with server implementations for all it's protocols.

An Example
----------

Let's write a JSON RPC Server::

    class Handler(object):
        def sayhi(self, person):
            return "Hi {0}".format(person)

    with Server("localhost", 7890, Handler()) as server:
        server.serve()

And your server is now running on localhost port 7890.

In production you'd probably want to use something other than the built in Python wsgiref simple_server, but the `server.app` method is a fully functional WSGI server ready for you to use with anything that supports WSGI.h
