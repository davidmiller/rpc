
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'gen-py')))

from rpc import thrifty

from service import Service

c = thrifty.Client(Service, "localhost", port = 4567)#
print c
