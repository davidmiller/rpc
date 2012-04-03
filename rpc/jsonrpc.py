"""

In addition to the normal parameters for Clients/Servers, the JSON RPC versions
contain a `verb` argument that allows you to specify either POST or GET as the
HTTP verb.
"""
import json
import uuid

import requests

from rpc import exceptions, clients, servers, chains

"""
Client Implementation
---------------------
"""

class Client(clients.RpcProxy):
    """
    This Proxy class implements a JSONRPC API.

    The timeout parameter will specify the ammount of time to wait for a call before
    raising an error.

    `verb` can be one of wither POST or GET, passed as a string and will determine
    which HTTP verb the client will use.

    >>> with Client("http://localhost:7890") as c:
    ...     print c.sayhi("Larry")
    "Hi Larry"
    """
    flavour = "JSON RPC"

    def __init__(self, url, timeout=3, verb="POST"):
        """
        Arguments:
        - `url`: string
        - `timeout`: number
        - `verb`: HTTP verb to use
        """
        self.url = url
        self.timeout = timeout
        self.verb = verb

    def __eq__(self, other):
        try:
            return self.url == other.url
        except AttributeError:
            return False

    def _get(self, headers, payload):
        """
        Make the call to a GET JSONRPC SERVER
        """
        return requests.get(self.url, params=payload, headers=headers,
                            timeout=self.timeout)

    def _post(self, headers, payload):
        """
        Make the call to a POST JSONRPC SERVER
        """
        return requests.post(self.url, data=payload, headers=headers,
                            timeout=self.timeout)

    def _build_payload(self, *args, **kwargs):
        """
        Build the Payload for our call.

        The first argument should be the method, the rest the arguments to the
        remote service call.

        Largely factored out as a convenient Hook fucntions
        """
        if kwargs:
            raise ValueError("Keyword arguments not supported by JSON RPC try passing a dict.")
        reqid = uuid.uuid4().hex
        method = args[1]
        params = args[2:]
        payload = dict(params=params, id=reqid, method=method)
        return reqid, dict([(k, json.dumps(v)) for k, v in payload.items()])

    def _apicall(self, *args, **kwargs):
        """
        Make a JSONRPC call to a JSONRPC server

        Arguments:
        - `data`: string
        """
        reqid, payload = self._build_payload(*args, **kwargs)
        headers = {'X-flavour': 'JSONRPC'}
        if self.verb == "GET":
            resp = self._get(headers, payload)
        elif self.verb == "POST":
            resp = self._post(headers, payload)
        else:
            raise ValueError("Unsupported HTTP Verb {verb}".format(verb=self.verb))
        return self._parse_resp(reqid, resp)

    def _parse_resp(self, reqid, resp):
        """
        Given a response from the server, let's parse it and check for errors.

        Arguments:
        - `reqid`: str
        - `resp`: requests.Response
        """
        result = json.loads(resp.text)
        if reqid != result['id']:
            raise exceptions.IdError("API Endpoint returned with id:{ret}, expecting:{exp}".format(
                ret=result['id'], exp=reqid))
        del result['id']
        if resp.status_code == 200:
            return result
        else:
            raise exceptions.RemoteException(result['result'])


def chain(*args, **kwargs ):
    """
    Will return an iterable which can be .chain()'ed as much as you
    like to create multiple Clients.

    >>> chain("localhost").chain("example.com")
    ... [<JSON RPC Client for localhost>, <JSON RPC Client for example.com>]
    """
    return chains.client_chain(Client, *args, **kwargs)

"""
Server Implementation
---------------------
"""

class Server(servers.HTTPServer):
    """
    A JSONRPC server

    >>> class Handler(object):
    ...     def sayhi(self, person):
    ...         return "Hi {0}".format(person)
    ...
    >>> with Server("localhost", 7890, Handler) as server:
    ...     server.serve()

    """
    flavour = "JSON RPC"

    def procedure(self, request):
        """
        JSON RPC procedure call - parse the params, call the procedure, and
        return the appropriate values.

        the procedure() method of HTTP Servers should return
        status, headers, content

        The request argument is a Web-Ob'ified WSGI request.
        """
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        result, error = None, None
        data = getattr(request, request.method)
        method, params, reqid = [json.loads(v) for v in [data.get('method', 'null'),
                                                         data.get('params', '[]'),
                                                         data.get('id', 'null')]]
        if not method:
            error = "No Method specified"
            return status, headers, dict(id=reqid, result=None, error=error)
        if not hasattr(self.handler, method):
            error = 'Method "{0}"" Not Found... '.format(method)
        if error:
            return status, headers, dict(id=id, result=result, error=error)
        try:
            result = getattr(self.handler, method)(*params)
        except Exception as err:
            error = '{error}: {msg}'.format(
                error=err.__class__.__name__, msg=err.message)
        return status, headers, dict(id=reqid, result=result, error=error)

    def parse_response(self, request, response):
        """
        Format the response:

        Just json.dump it
        """
        return json.dumps(response)
