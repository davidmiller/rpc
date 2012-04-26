.. _rpctl:

============================
Controlling your RPC Servers
============================

A generic pattern for controling RPC servers.

Having written a server implementation, we often want to run those servers.

While running from a shell is fine for a while, and many people will want to embed in a WSGI environment, other times, you just want a simle server daemon without too much fuss.

If this is your thing, then the rpc.control module is for you.

The Configuration File
======================

RPC-based servers need a configuration file.

This can be called/placed anywhere you like, but must be in .ini format:
:

    [rpctl]
    host = 0.0.0.0
    port = 4567
    handler = mymodule.Handler
    server = rpc.jsonrpc.Server

Generate From $ rpctl generate
------------------------------

Include in existing config files
--------------------------------

Because rpctl will only ever look inside the `rpctl` section of your config
file, you can use the same file for all/any of your own configurations as well!



Using $ rpctl
=============

rpctl is a generic RPC server control program.


