"""
rpc.jsonp

A JSONP server for your handlers!
"""
import json

from rpc import servers

class Server(servers.HTTPServer):
    """
    A JSONP Server

    >>> with Server('localhost', 8080, object) as server:
    ...     server.serve()
    """
    flavour = "JSONP"

    def parse_response(self, request, response):
        """
        Format the response:

        Deal with the 'callback' paramater!
        """
        resp = "{callback}({data})".format(callback=request.GET['callback'],
                                           data=json.dumps(response))
        return resp


