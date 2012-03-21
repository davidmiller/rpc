
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'gen-py')))

from rpc import thrifty

from service import Service

class Handler(object):
    def ping(self):
        return "PONG!"


if __name__ == '__main__':
    server = thrifty.Server(port=4567, handler=Handler, service=Service)
    server.serve()
