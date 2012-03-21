
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'gen-py')))

from rpc import thrifty

from service import Service

with thrifty.Client("localhost:4567", Service) as c:
    print c.ping()
