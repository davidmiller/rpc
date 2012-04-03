"""
rpc.servers

Base class for server implementations
"""
import functools
import socket
from wsgiref import simple_server

import webob

from rpc import exceptions

def webobify(fn):
    "Decorator to convert a WSGI environ into a WebOb Request"

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

    def scaffold(self):
        """
        This hook function is called with no arguments as the last item
        of initialisation. This is an excellent subclass choice for instance
        building code.

        In this base class, is simply a no-op
        """
        return

    def serve(self):
        """
        Subclasses should override this base method to accept incoming
        calls and deal with marshalling/dispatch.
        """
        raise NotImplementedError()


class HTTPServer(Server):
    """
    A WSGI based HTTP Server class.

    Subclasses of HTTPServer should define two methods, `procedure` and `parse_response`.
    """

    def __init__(self, *args, **kwargs):
        super(HTTPServer, self).__init__(*args, **kwargs)
        try:
            self.httpd = simple_server.make_server(self.host, self.port, self.app)
        except socket.error as err:
            if err.errno == 98:
                raise exceptions.PortInUseError("Port {0} is already in use on {1}".format(
                    self.port, self.host))

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
        Our JSON RPC WSGI App.

        Decode and deserialize the POST data, locate the handler method,
        ascertain the result and then return our JSON response.
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
        print("Serving {flavour} on {host}:{port}".format(
                flavour=self.flavour, host=self.host, port=self.port))
        self.httpd.serve_forever()

