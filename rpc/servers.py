"""
rpc.servers

Base class for server implementations

"""
import functools
import socket
from wsgiref import simple_server

import webob

from rpc import daemon, exceptions

def webobify(fn):
    """
    Decorator to convert a method that expects a
    WSGI environ into a WebOb Request
    """

    @functools.wraps(fn)
    def munger(self, environ, start):
        return fn(self, webob.Request(environ), start)

    return munger

class Server(object):
    """
    Base class for servers.

    Servers are initialised as contextmanagers in order to ensure the freeing of
    resources.

    >>> with Server('localhost', 8888, object) as s:
    ...     s.serve()

    The `close` method of a server instance is guaranteed to be called during
    shutdown using this method.

    Otherwise, the User takes full responsibility for the freeing of resouces.

    Don't do this.
    """
    flavour = 'Base'

    def __init__(self, host=None, port=None, handler=None):
        """
        Arguments:
        - `host`: string
        - `port`: int
        - `handler`: callable
        """
        self.host = host
        self.port = port
        self.handler = handler()
        self.scaffold()

    def __repr__(self):
        return "<{flavour} Server on {host}:{port} calling {handler}>".format(
            flavour=self.flavour, host=self.host, port=self.port,
            handler=self.handler.__class__.__name__)

    def __eq__(self, other):
        try:
            return self.flavour == other.flavour and self.host == other.host \
              and self.port == other.port and \
              self.handler.__class__ == other.handler.__class__
        except AttributeError:
            return False

    def __del__(self):
        """
        By default we call self.close()
        """
        self.close()
        return

    def __enter__(self):
        return self

    def __exit__(self, exc, type, stack):
        self.close()
        return

    def scaffold(self):
        """
        This hook function is called with no arguments as the last item
        of initialisation. This is an excellent subclass choice for instance
        building code.

        In this base class, is simply a no-op
        """
        return

    def close(self):
        """
        This hook function is called with no items as the last item
        of object deletion.

        This is an excellent choice of method to subclass for those
        servers wishing to free resources.
        """
        return

    def procedure(self,*args, **kwargs):
        """
        This hook function is called in order to dispatch the incoming call into
        it's target method.
        """
        raise NotImplementedError()

    def serve(self):
        """
        This hook function is intended for Subclasses to
        override in order to accept incoming
        calls and deal with marshalling/dispatch.
        """
        raise NotImplementedError()


class HTTPServer(Server):
    """
    A WSGI based HTTP Server class.

    Subclasses of HTTPServer should define two methods, `procedure` and `parse_response`.
    """
    flavour = "HTTP Server"

    def close(self):
        """
        Close our active port binding
        """
        if hasattr(self, 'httpd'):
            print 'closes!'
            self.httpd.socket.close()

    def parse_response(self, request, response):
        """
        No-op hook for subclasses to override.
        """
        return response

    @webobify
    def app(self, request, start_response):
        """
        Our HTTP based WSGI RPC application

        Decode and deserialize the POST data, locate the handler method,
        ascertain the result and then return our response.
        """
        if request.method not in ['GET', 'POST']:
            return ["Invalid HTTP Verb {verb}".format(verb=request.method)]
        status, headers, response = self.procedure(request)
        start_response(status, headers)
        return [self.parse_response(request, response)]

    def serve(self):
        """
        Start handling requests.

        It a Sub-Optimal idea to use this in any kind of production setting.
        """
        try:
            self.httpd = simple_server.make_server(self.host, self.port, self.app)
        except socket.error as err:
            if err.errno == 98:
                raise exceptions.PortInUseError("Port {0} is already in use on {1}".format(
                    self.port, self.host))

        print("Serving {flavour} on {host}:{port}".format(
                flavour=self.flavour, host=self.host, port=self.port))
        self.httpd.serve_forever()

    def procedure(self, request):
        """
        This hook function is called in order to dispatch the incoming call into
        it's target method.

        It is called with a single argument, which is a WebOb Request onject compriing a WSGI
        environ.
        """
        raise NotImplementedError()

class ServerDaemon(daemon.Daemon):
    """
    Implements a well behaved UNIX Daemon to run our Servers.
    """

    def __init__(self, server, pidfile, **kwargs):
        """
        Stores the server instance we want to operate on, and sets up the
        pidfile and other daemon variables.
        """
        daemon.Daemon.__init__(self, pidfile, **kwargs)
        self.server = server
        self.pidfile = pidfile

    def run(self):
        """
        Implement the final hook of our Daemon class - actually serving
        requests with the server!
        """
        self.server.serve()


