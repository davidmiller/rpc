"""
remotes.json

Provide JSONRPC and JSONP implementations
"""
import cgi
import json
import uuid
from wsgiref import simple_server

import requests

from rpc import exceptions

class Client(object):
    """
    This Proxy class implements a JSONRPC API
    """

    def __init__(self, url, timeout=3):
        """
        Arguments:
        - `url`: string
        - `timeout`: number
        """
        self.url = url
        self.timeout = timeout

    def __repr__(self):
        return "<JSON RPC Client for {url}>".format(url=self.url)

    def __eq__(self, other):
        try:
            return self.url == other.url
        except AttributeError:
            return False

    def __getattr__(self, key):
        """
        We allow anything not in self.__dict__ to be called as a method.
        abstracting the reqests away.
        """
        if key in self.__dict__:
            return self.__dict__[key]
        return lambda *a, **kw: self._apicall(key, *a, **kw)

    def _apicall(self, method, *args, **kwargs):
        """
        Make a JSONRPC call to a JSONRPC server

        Arguments:
        - `data`: string
        """
        reqid = uuid.uuid4().hex
        payload = dict(args=args, kwargs=kwargs, method=method, id=reqid)
        payload = {k: json.dumps(v) for k, v in payload.items()}
        headers = {'X-flavour': 'JSONRPC'}
        resp = requests.post(
            self.url, data=payload, timeout=self.timeout)
        print resp.text
        result = json.loads(resp.text)
        if reqid != result['id']:
            raise exceptions.IdError("API Endpoint returned with id:{ret}, expecting:{exp}".format(
                ret=result['id'], exp=reqid))
        del result['id']
        return result['result']


class Server(object):
    "A JSONRPC server"

    def __init__(self, host=None, port=None, handler=None):
        """
        Arguments:
        - `host`: string
        - `port`: int
        """
        self.host = host
        self.port = port
        self.handler = handler
        self.httpd = simple_server.make_server(host, port, self.json_app)

    def json_app(self, environ, start_response):
        """
        Our JSON RPC WSGI App
        """
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ,
                                keep_blank_values=True)
        method, args, kwargs = [json.loads(v) for v in [post.getvalue('method'),
                                                        post.getvalue('args'),
                                                        post.getvalue('kwargs')]]
        result = getattr(self.handler, method)(*args, **kwargs)
        status = '200 OK'
        response_headers = [('Content-Type', 'application/json')]
        start_response(status, response_headers)
        response = dict(id=json.loads(post.getvalue('id')),
                        result=result)
        return [json.dumps(response)]

    def serve(self):
        """
        Start handling requests
        """
        print("Serving JSON RPC on {host}:{port}".format(
            host=self.host, port=self.port))
        self.httpd.serve_forever()

